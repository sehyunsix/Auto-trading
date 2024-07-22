import tensorflow as tf
import keras
from action_maker.data.dataCollector import DataCollector


class LstmTrainer(keras.Model):

    def __init__(dataCollector: DataCollector, model, scaler):
        super().__init__()
        self.model = model
        self.scaler = scaler
        self.inputs = scaler.fit_transform(dataCollector.get_train_data())
        self.ouputs = scaler.fit_transform(dataCollector.get_train_data())

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

    @property
    def metrics(self):
        # List metrics here.
        return [self.accuracy_metric]

    def call(self, x):
        # Equivalent to `call()` of the wrapped keras.Model
        x = self.model(x)
        return x
