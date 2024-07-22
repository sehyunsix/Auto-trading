from action_maker.logger.timeLogger import logging_time
from action_maker.data.env import DATA_BASE_URL, DATE_FORMAT

import psycopg2
from datetime import datetime
import numpy as np
import pickle


class DataCollector:
    raw_data = []
    train_data = []
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

    def get_index_with_date(self, target, data):
        stack = [(0, len(data) - 1)]
        while stack:
            start, end = stack.pop()
            mid = (start + end) // 2
            if mid < 0 or mid > len(data) - 1:
                raise ValueError("No target date in range")
            current = data[mid][0]
            if target == current:
                return mid
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
        self.raw_data = pickle.load(open("raw_data.pkl", "rb"))

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
    ):

        assert len(self.raw_data) != 0, "raw_data is None"

        raw_data = self.get_data_range_with_date(start_time, end_time, self.raw_data)

        train_data = [
            raw_data[i : i + window_size, 1 : feature_size + 1]
            for i in range(0, len(raw_data) - window_size + 1, sliding_size)
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

        self.train_data_x = train_data[:, :-predict_size, :]
        self.train_data_y = train_data[:, -predict_size:, :]
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
        assert len(self.test_data_x) != 0, "train_data is None"
        assert len(self.test_data_y) != 0, "train_data is None"
        return self.train_data_x, self.train_data_y, self.test_data_x, self.test_data_y


if __name__ == "__main__":
    data_collector = DataCollector()

    # recieve data test

    # data_collector.make_raw_data("2023-01-01 00:00:00", "2023-01-02 00:00:00")
    data_collector.load_raw_data()

    # data_collector.save_raw_data()

    # make train data test
    data_collector.make_train_data(
        start_time="2023-01-01 00:01:00",
        end_time="2023-01-02 00:00:00",
        window_size=90,
        predict_size=15,
        sliding_size=1,
        feature_size=1,
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
