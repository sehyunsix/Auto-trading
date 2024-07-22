from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.optimizers import Adam
import tensorflow.keras as keras


def create_model(sequence_length):
    model = Sequential()
    model.add(LSTM(64, return_sequences=True, input_shape=(sequence_length, 1)))
    model.add(LSTM(64, input_shape=(sequence_length, 1)))
    model.add(Dense(1))
    model.compile(optimizer=Adam(learning_rate=0.001), loss="mean_squared_error")
    return model


if __name__ == "__main__":
    model = create_model(90)
    model.summary()
    model.save("model.h5")
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
