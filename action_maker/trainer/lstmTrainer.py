from action_maker.data.dataCollector import DataCollector
from action_maker.model import lstmModel
from action_maker.logger.timeLogger import logging_time

import tensorflow as tf
import numpy as np
import keras
from tensorflow.keras import ops
from sklearn.preprocessing import MinMaxScaler
import wandb
from wandb.integration.keras import WandbMetricsLogger, WandbModelCheckpoint


class LstmTrainer(keras.Model):

    def __init__(self, dataCollector: DataCollector, model):
        super().__init__()
        self.model = model

    def train_step(self, data):
        x, y = data
        with tf.GradientTape() as tape:
            y_pred = self.model(x, training=True)
            loss = self.compiled_loss(y, y_pred)
        # Compute gradients
        trainable_vars = self.trainable_variables
        gradients = tape.gradient(loss, trainable_vars)

        # Update weights
        self.optimizer.apply_gradients(zip(gradients, trainable_vars))

        # Update metrics
        for metric in self.metrics:
            metric.update_state(y, y_pred)

        # Return a dict mapping metric names to current value.
        return {m.name: m.result() for m in self.metrics}

    def test_step(self, data):
        x, y = data

        # Inference step
        y_pred = self.model(x, training=False)

        # Update metrics
        for metric in self.metrics:
            metric.update_state(y, y_pred)
        return {m.name: m.result() for m in self.metrics}

    def inverse_mae_metric(self, y_true, y_pred):
        print(y_true)
        print(y_pred)
        min = tf.constant(dataCollector.scaler.data_min_, dtype=tf.float32)
        max = tf.constant(dataCollector.scaler.data_max_, dtype=tf.float32)

        inverse_y_true = min + y_true * (max - min)
        inverse_y_pred = min + y_pred * (max - min)

        return tf.keras.losses.MAPE(inverse_y_true, inverse_y_pred)

    def inverse_mape_metric(self, y_true, y_pred):
        print(y_true)
        print(y_pred)
        min = tf.constant(dataCollector.scaler.data_min_, dtype=tf.float32)
        max = tf.constant(dataCollector.scaler.data_max_, dtype=tf.float32)

        inverse_y_true = min + y_true * (max - min)
        inverse_y_pred = min + y_pred * (max - min)

        return tf.keras.losses.MSE(inverse_y_true, inverse_y_pred)

    def inverse_mse_metric(self, y_true, y_pred):
        print(y_true)
        print(y_pred)
        min = tf.constant(dataCollector.scaler.data_min_, dtype=tf.float32)
        max = tf.constant(dataCollector.scaler.data_max_, dtype=tf.float32)

        inverse_y_true = min + y_true * (max - min)
        inverse_y_pred = min + y_pred * (max - min)

        return tf.keras.losses.MAE(inverse_y_true, inverse_y_pred)

    def call(self, x):
        # Equivalent to `call()` of the wrapped keras.Model
        x = self.model(x)
        return x

    def save_model(self, path):
        self.model.save(path)


if __name__ == "__main__":
    print("lstmTrainer Test start..")
    gpu = len(tf.config.list_physical_devices("GPU")) > 0
    print("GPU is", "available" if gpu else "NOT AVAILABLE")

    dataCollector = DataCollector()
    dataCollector.load_raw_data()
    dataCollector.make_train_data(
        start_time="2021-01-01 00:00:00",
        end_time="2023-12-31 23:59:00",
        window_size=105,
        predict_size=15,
        sliding_size=1,
        feature_size=1,
        train_ratio=0.8,
        scaler=MinMaxScaler(),
    )

    model = lstmModel.create_model_output_15()
    lstmTrainer = LstmTrainer(dataCollector, model)
    wandb.init(
        project="Auto-trading",
        config={
            "model": "lstm",
            "window_size": 91,
            "predict_size": 1,
            "sliding_size": 1,
            "feature_size": 1,
            "train_ratio": 0.8,
        },
    )
    optimizer = keras.optimizers.Adam(0.01)
    lstmTrainer.compile(
        optimizer=optimizer,
        loss="mse",
        metrics=[
            lstmTrainer.inverse_mae_metric,
            lstmTrainer.inverse_mape_metric,
            lstmTrainer.inverse_mse_metric,
        ],
    )

    x_train, y_train = dataCollector.get_train_data()
    validation_data = dataCollector.get_vaildate_data()

    lstmTrainer.fit(
        x=x_train,
        y=y_train,
        validation_data=validation_data,
        batch_size=256,
        epochs=3,
        callbacks=[
            WandbMetricsLogger(
                log_freq=10,
            ),
        ],
        shuffle=True,
    )
    lstmTrainer.save_model("action_maker/model/model_output_15_1.h5")
