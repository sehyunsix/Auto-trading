from typing import Dict

import wandb.plot
from action_maker.data.dataCollector import DataCollector, SimulateData
from action_maker.data.env import DATE_FORMAT
from action_maker.model import lstmModel

import wandb
import tensorflow as tf
from wandb.integration.keras import WandbMetricsLogger, WandbEvalCallback
import numpy as np
import matplotlib.pyplot as plt
import time
from tqdm import tqdm

tf.debugging.set_log_device_placement(False)


class LstmSimulator:

    def __init__(
        self,
        dataCollector: DataCollector,
        simulator_data: SimulateData,
        model,
        batch_size=1024,
    ):
        super().__init__()
        self.model = model
        self.dataCollector = dataCollector
        self.simulate_data = simulator_data
        self.batch_size = batch_size

    def prediction(self):
        # simulate_table = wandb.Table(
        #     columns=["idx", "datetime", "source", "target", "pred"]
        # )
        for idx, data in enumerate(tqdm(self.simulate_data)):
            # print(data)
            source, target = data
            # print(source.shape)
            source = tf.convert_to_tensor(source, dtype=tf.float32)

            pred = self.model(source, training=False)

            print("loss : ", tf.keras.losses.MSE(target, pred).numpy().mean())

            min = tf.constant(dataCollector.scaler.data_min_, dtype=tf.float32)
            max = tf.constant(dataCollector.scaler.data_max_, dtype=tf.float32)

            source = min + source * (max - min)
            target = min + target * (max - min)
            pred = min + pred * (max - min)
            pred = np.expand_dims(pred, axis=2)

            # print(source.shape)
            # print(target.shape)
            # print(pred.shape)

            # line1 = np.concatenate([source, target], axis=1)
            # line2 = np.concatenate([source, pred], axis=1)

            # line1 = np.squeeze(line1, axis=2)
            # line2 = np.squeeze(line2, axis=2)

            # draw_line_1 = plt.plot(
            #     self.simulate_data.time[idx : idx + len(line1[0])],
            #     line1[0],
            #     label="target",
            # )
            # draw_line_2 = plt.plot(
            #     self.simulate_data.time[idx : idx + len(line2[0])],
            #     line2[0],
            #     label="pred",
            # )
            # plt.legend()
            # plt.show(block=False)
            # plt.pause(1)
            # plt.cla()

            # wandb.log(
            #     {
            #         "plot_pridict": wandb.plot.line_series(
            #             xs=simulate_data.time[idx : idx + len(line1[0])],
            #             ys=[line1, line2],
            #         )
            #     }
            # )


if __name__ == "__main__":
    dataCollector = DataCollector()
    dataCollector.load_raw_data()
    # wandb.init(project="Auto-trading")
    simulate_data = dataCollector.make_simulate_data(
        start_time="2021-01-01 00:00:00",
        end_time="2023-12-31 23:59:00",
        window_size=105,
        predict_size=15,
        sliding_size=1,
        feature_size=1,
        batch_size=128,
    )
    # wandb.init(project="Auto-trading")
    model = lstmModel.create_model_output_15()
    model.load_weights("action_maker/model/model_output_15_1.h5")
    model.compile(loss="mse", metrics=["mse", "mae"])
    simulator = LstmSimulator(dataCollector, simulate_data, model, batch_size=128)
    simulator.prediction()
