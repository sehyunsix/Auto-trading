from action_maker.logger.timeLogger import logging_time
from action_maker.data.env import DATA_BASE_URL, DATE_FORMAT

from sklearn.preprocessing import MinMaxScaler
import psycopg2
from datetime import datetime
from tensorflow.keras.utils import Sequence
import numpy as np
import pickle
from tqdm import tqdm


class Scaler:
    def __init__(self):
        self.data_min_ = None
        self.data_max_ = None

    def fit(self, data):
        self.data_min_ = np.min(data, axis=0)
        self.data_max_ = np.max(data, axis=0)

    def transform(self, data):
        return (data - self.data_min_) / (self.data_max_ - self.data_min_)

    def inverse_transform(self, data):
        return data * (self.data_max_ - self.data_min_) + self.data_min_


class SimulateData:
    def __init__(self, time, source, target, batch_size):
        self.time = time
        self.source = np.array_split(
            source[: len(source) // batch_size * batch_size], len(source) // batch_size
        )
        self.target = np.array_split(
            target[: len(target) // batch_size * batch_size], len(target) // batch_size
        )

        print(
            "time : ",
            len(self.time),
            "source : ",
            len(self.source[0]),
            "target : ",
            len(self.target[0]),
        )

    def __repr__(self):
        return f"time : {self.time} source : {self.source} target : {self.target}"

    def __len__(self):
        return len(self.source)

    def __getitem__(self, idx):
        return self.source[idx], self.target[idx]

    def __iter__(self):
        self.current = 0
        return self

    def __next__(self):
        if self.current < len(self):
            item = self[self.current]
            self.current += 1
            return item
        else:
            raise StopIteration


class DataCollector:
    scaler = None
    raw_data = []
    train_data = []
    scaled_data = []
    train_data_x = []
    train_data_y = []
    test_data_x = []
    test_data_y = []

    def is_valid_date(self, date_string, date_format):
        try:
            datetime.strptime(date_string, date_format)
            return True
        except ValueError:
            return False

    @logging_time
    def get_index_with_date(self, target, data):
        stack = [(0, len(data) - 1)]
        while stack:
            start, end = stack.pop()
            mid = (start + end) // 2
            current = data[mid][0]
            if target == current:
                return mid
            if mid <= 0 or mid >= len(data) - 1:
                raise ValueError("No target date in range")
            elif target < current:
                stack.append((start, mid - 1))
            else:
                stack.append((mid + 1, end))

    def get_data_range_with_date(self, start_time, end_time, data):
        start_time = datetime.strptime(start_time, DATE_FORMAT)
        end_time = datetime.strptime(end_time, DATE_FORMAT)
        try:
            start_index = self.get_index_with_date(start_time, data)
            end_index = self.get_index_with_date(end_time, data)
        except ValueError:
            raise ValueError("date is not valid")

        return data[start_index : end_index + 1]

    @logging_time
    def make_raw_data(self, start_time, end_time):
        # assert self.raw_data == None, "raw_data is not None"

        CONNECTION = DATA_BASE_URL

        self.is_valid_date(start_time, DATE_FORMAT)
        self.is_valid_date(end_time, DATE_FORMAT)

        with psycopg2.connect(CONNECTION) as conn:
            with conn.cursor() as cur:
                print("get data from db...")
                cur.execute(
                    f"SELECT open_time, open_price FROM ethusdt WHERE open_time >= '{start_time}' AND open_time <= '{end_time}' ORDER BY open_time"
                )
                result = cur.fetchall()
                print(f"get data complete recive {len(result)} data")
                self.raw_data = np.array(result)

    @logging_time
    def save_raw_data(self):
        pickle.dump(self.raw_data, open("raw_data.pkl", "wb"))

    @logging_time
    def save_train_data(self):
        pickle.dump(self.train_data, open("train_data.pkl", "wb"))

    @logging_time
    def load_raw_data(self):
        print("load raw data")
        self.raw_data = pickle.load(open("raw_data.pkl", "rb"))
        print(self.raw_data[0], self.raw_data[-1])

    @logging_time
    def load_train_data(self):
        self.train_data = pickle.load(open("train_data.pkl", "rb"))

    @logging_time
    def make_train_data(
        self,
        start_time,
        end_time,
        window_size: int,
        predict_size: int,
        sliding_size: int,
        feature_size: int,
        train_ratio: float = 0.8,
        scaler=None,
    ):

        assert len(self.raw_data) != 0, "raw_data is None"

        print("get_data_range_with_date")
        raw_data = self.get_data_range_with_date(start_time, end_time, self.raw_data)

        if scaler != None:
            print("********* scale train data ***********")
            self.scaler = scaler
            self.scaler.fit(raw_data[:, 1 : feature_size + 1])
            print(
                "original_data_min : ",
                self.scaler.data_min_,
                "original_data_max : ",
                self.scaler.data_max_,
            )
            print("scale now...")
            scaled_raw_data = self.scaler.transform(raw_data[:, 1:])
            print(
                "scaled_data_min : ",
                min(scaled_raw_data),
                "scaled_data_max : ",
                max(scaled_raw_data),
            )
            inverse_raw_data = self.scaler.inverse_transform(scaled_raw_data)
            print(
                "inverse_data_min : ",
                min(inverse_raw_data),
                "inverse_data_max : ",
                max(inverse_raw_data),
            )

            raw_data[:, 1 : feature_size + 1] = scaled_raw_data

        train_data = [
            raw_data[i : i + window_size, 1 : feature_size + 1]
            for i in tqdm(range(0, len(raw_data) - window_size + 1, sliding_size))
        ]

        ## remove the last data to make the train_data size to be multiple of window_size

        assert (
            len(train_data) == (len(raw_data) - window_size + 1) // sliding_size
        ), f"train_data is not valid {len(train_data)} != {(len(raw_data) - window_size + 1) // sliding_size}"

        train_data = np.array(train_data)

        assert len(train_data.shape) == 3, "train_data shape is not valid"

        assert (
            train_data.shape[2] == feature_size
        ), f"train_data feature size is not valid  {train_data.shape}"

        assert (
            train_data.shape[1] == window_size
        ), f"train_data window size is not valid  {train_data.shape}"

        self.train_data_x = train_data[:, :-predict_size, :].astype("float32")
        self.train_data_y = train_data[:, -predict_size:, :].astype("float32")
        assert (
            self.train_data_x.shape[1] == window_size - predict_size
        ), "train_data_x shape is not valid"
        assert (
            self.train_data_y.shape[1] == predict_size
        ), "train_data_y shape is not valid"

        slicing_index = int(len(self.train_data_x) * train_ratio)

        self.train_data_x, self.test_data_x = np.split(
            self.train_data_x, [slicing_index], axis=0
        )
        self.train_data_y, self.test_data_y = np.split(
            self.train_data_y, [slicing_index], axis=0
        )

        print("********* proccessed data ***********")

        print("start_time : ", start_time)
        print("end_time : ", end_time)
        print("window_size : ", window_size)
        print("predict_size : ", predict_size)
        print("sliding_size : ", sliding_size)
        print("feature_size : ", feature_size)
        print("train_data_x : ", self.train_data_x.shape)
        print("test_data_x : ", self.test_data_x.shape)
        print("train_data_y : ", self.train_data_y.shape)
        print("test_data_y : ", self.test_data_y.shape)

    def get_train_data(self):
        assert len(self.train_data_x) != 0, "train_data is None"
        assert len(self.train_data_y) != 0, "train_data is None"
        return self.train_data_x, self.train_data_y

    def get_vaildate_data(self):
        assert len(self.test_data_x) != 0, "test_data is None"
        assert len(self.test_data_y) != 0, "test_data is None"
        return self.test_data_x, self.test_data_y

    def make_simulate_data(
        self,
        start_time,
        end_time,
        predict_size,
        window_size,
        feature_size,
        sliding_size,
        batch_size,
        scaler=MinMaxScaler(),
    ):
        self.scaler = scaler

        raw_data = self.get_data_range_with_date(start_time, end_time, self.raw_data)
        scaler.fit(raw_data[:, 1:2])
        raw_data[:, 1:2] = self.scaler.transform(raw_data[:, 1:2])

        simulate_data = [
            raw_data[i : i + window_size, 1 : feature_size + 1]
            for i in tqdm(range(0, len(raw_data) - window_size + 1, sliding_size))
        ]

        simulate_data = np.array(simulate_data)

        simulateData = SimulateData(
            raw_data[: len(raw_data) - window_size + 1, 0],
            simulate_data[:, :-predict_size, :].astype(np.float32),
            simulate_data[:, -predict_size:, :].astype(np.float32),
            batch_size,
        )
        assert len(simulateData.target) == len(simulateData.source)
        return simulateData


if __name__ == "__main__":
    data_collector = DataCollector()

    # recieve data test

    # data_collector.make_raw_data("2021-01-01 00:00:00", "2024-01-01 00:00:00")
    data_collector.load_raw_data()

    # data_collector.save_raw_data()

    # make train data test
    data_collector.make_simulate_data(
        start_time="2021-01-01 00:00:00",
        end_time="2023-12-31 23:59:00",
        window_size=91,
        predict_size=1,
        sliding_size=1,
        feature_size=1,
        scaler=MinMaxScaler(),
    )

    # # save data test

    # data_collector.save_raw_data()
    # data_collector.save_train_data()

    # # raw data test

    # data_collector.load_raw_data()
    # data_collector.load_train_data()

    ## get date date test
    # print(
    #     data_collector.get_data_range_with_date(
    #         "2023-01-01 00:01:00", "2023-01-02 00:00:00", data_collector.raw_data
    #     )
    # )
