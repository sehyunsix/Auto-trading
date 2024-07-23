from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Input
from tensorflow.keras.optimizers import Adam
import tensorflow.keras as keras


def create_model_output():
    model = Sequential()
    model.add(Input(shape=(90, 1)))
    model.add(LSTM(64, return_sequences=True))
    model.add(Dense(1))
    return model


def create_model_output_15():
    model = Sequential()
    model.add(Input(shape=(90, 1)))
    model.add(LSTM(64, return_sequences=True))
    model.add(LSTM(64, return_sequences=True))
    model.add(LSTM(32))
    model.add(Dense(15))
    return model


if __name__ == "__main__":
    model = create_model_output_15()
    model.summary()
    model.load_weights("action_maker/model/model_output_15_1.h5")
    # The line `# model.predict()` is a commented-out line in the code. This means
    # that it is not being executed when the code runs. It is likely there for
    # reference or as a placeholder for where you might want to add code to make
    # predictions using the model.
    keras.utils.plot_model(
        model,
        to_file="model.png",
        show_shapes=False,
        show_dtype=False,
        show_layer_names=False,
        rankdir="TB",
        expand_nested=False,
        dpi=200,
        show_layer_activations=False,
    )
