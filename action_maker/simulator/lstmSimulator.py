from typing import Dict

from action_maker.data.dataCollector import DataCollector, SimulateData
from action_maker.logger.test import init_logger
from action_maker.data.env import DATE_FORMAT
from action_maker.model import lstmModel


import wandb
import tensorflow as tf
from wandb.integration.keras import WandbMetricsLogger, WandbEvalCallback
import numpy as np
import matplotlib.pyplot as plt
import time
from tqdm import tqdm
from dataclasses import dataclass, asdict
from datetime import date, datetime, timedelta
import logging
from logging import Logger


tf.debugging.set_log_device_placement(False)


@dataclass
class Symbol:
    name: str
    quantity: float


@dataclass
class HoldingState:
    symbol: Symbol
    buy_price: float
    now_price: float
    buy_time: date


@dataclass
class State:
    totalMoney: float
    holdingState: HoldingState
    yieldState: float
    timeState: date


@dataclass
class Action:
    side: str
    symbol: Symbol
    time: date


class LstmSimulator:

    def __init__(
        self,
        dataCollector: DataCollector,
        simulator_data: SimulateData,
        start_state: State,
        model,
        batch_size: int,
        logger: Logger,
    ):
        super().__init__()
        self.model = model
        self.dataCollector = dataCollector
        self.simulate_data = simulator_data
        self.state = start_state
        self.start_state = start_state
        self.batch_size = batch_size
        self.logger = logger
        self.prediction_list = []
        self.target_list = []
        self.price_list = []

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
            self.logger.info(
                "loss : %s", tf.keras.losses.MSE(target, pred).numpy().mean()
            )

            min = tf.constant(dataCollector.scaler.data_min_, dtype=tf.float32)
            max = tf.constant(dataCollector.scaler.data_max_, dtype=tf.float32)

            source = min + source * (max - min)
            target = min + target * (max - min)
            pred = min + pred * (max - min)
            pred = np.expand_dims(pred, axis=2)
            self.prediction_list.extend(pred)
            self.target_list.extend(target)
            self.price_list.extend(source[:, -1, :].numpy())

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

    def action(
        self,
        pred: list,
        target: list,
        state: State,
        losslimit: float,
        timelimit: float,
        price: float,
    ):
        result = Action("", "", state.timeState)
        if state.holdingState.symbol.name == "usdt":
            if pred[-1] > pred[0] * 1.00001:
                result.side = "buy"
                result.symbol = Symbol("eth", self.state.totalMoney / price)
                result.time = state.timeState

        elif state.holdingState.now_price < state.holdingState.buy_price * (
            1 - losslimit
        ):
            result.side = "sell"
            result.symbol = Symbol("eth", state.holdingState.symbol.quantity)
            result.time = state.timeState

        elif state.timeState > state.holdingState.buy_time + timedelta(
            minutes=timelimit
        ):

            result.side = "sell"
            result.symbol = Symbol("eth", state.holdingState.symbol.quantity)
            result.time = state.timeState

        if result.side != "":
            self.logger.debug(
                "action:  %s  prediction : %.5f %.5f", asdict(result), pred[1], pred[-1]
            )

        return result

    def update_state(self, result: Action, price: float):
        if result.side == "sell":
            self.state.holdingState.symbol.quantity = (
                self.state.holdingState.symbol.quantity - result.symbol.quantity
            )
            if self.state.holdingState.symbol.quantity < 0.0001:
                self.state.holdingState.symbol.quantity = 0
                self.state.holdingState.symbol.name = "usdt"
                self.state.holdingState.symbol.quantity = result.symbol.quantity * price

        if result.side == "buy":
            self.state.holdingState.symbol = result.symbol

        if self.state.holdingState.symbol.name == "usdt":
            self.state.holdingState.now_price = 1
        else:
            self.state.holdingState.now_price = price
        self.state.totalMoney = (
            self.state.holdingState.now_price * self.state.holdingState.symbol.quantity
        )

    def do_action(
        self,
    ):
        """
        make action every 15 miniutes for pridiction data
        buy: if pridiction price is lower then price
        sell: if 15 miniutes after, or now price is lower than boundary.
        """
        self.logger.info("%s", asdict(self.start_state))
        for pred, target, price in zip(
            self.prediction_list, self.target_list, self.price_list
        ):
            result = self.action(pred, target, self.state, 0.05, 15, price)
            self.update_state(result, price)
            self.state.timeState = self.state.timeState + timedelta(minutes=1)
            self.logger.info("%s", asdict(self.state))
        return 0


if __name__ == "__main__":
    init_logger()
    mylogger = logging.getLogger("my")
    mylogger.info("start siulator")
    dataCollector = DataCollector()
    dataCollector.load_raw_data()
    # wandb.init(project="Auto-trading")
    simulate_data = dataCollector.make_simulate_data(
        start_time="2023-12-01 00:00:00",
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
    simulator = LstmSimulator(
        dataCollector=dataCollector,
        simulator_data=simulate_data,
        start_state=State(
            1,
            HoldingState(Symbol("usdt", 1), 1, 1, simulate_data.time[0]),
            0,
            simulate_data.time[0],
        ),
        model=model,
        batch_size=128,
        logger=mylogger,
    )
    simulator.prediction()
    simulator.do_action()
