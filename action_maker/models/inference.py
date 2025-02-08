import requests
from datetime import datetime, timedelta
import time
import pandas as pd
import numpy as np
from models.get_price import get_data
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.optimizers import Adam

def create_model(sequence_length):
    model = Sequential()
    model.add(LSTM(64, return_sequences=True, input_shape=(sequence_length, 1)))
    model.add(LSTM(64))
    model.add(Dense(1))
    model.compile(optimizer=Adam(learning_rate=0.001), loss='mean_squared_error')
    return model

def predict_future(model, input_data, future_steps, scaler, sequence_length):
    predictions = []
    current_input = input_data[-sequence_length:]
    
    for _ in range(future_steps):
        current_input = current_input.reshape((1, sequence_length, 1))
        prediction = model.predict(current_input, verbose=0)
        predictions.append(prediction[0, 0])
        current_input = np.append(current_input[0][1:], prediction[0, 0])
        
    return scaler.inverse_transform(np.array(predictions).reshape(-1, 1))

# def predict_btc_prices_socket(received_data):

#     if len(received_data) == 0:
#         raise ValueError("No data received from WebSocket")
#     if len(received_data) < 90:
#         raise ValueError("Please wait a second ^^. Not enough data received from WebSocket")

#     close_prices = [float(data['data']['p']) for data in received_data]

#     btc_data = pd.DataFrame(close_prices, columns=['close'])
#     # print("btc : ",btc_data)
    
#     scaler = MinMaxScaler()
#     scaled_data = scaler.fit_transform(btc_data)
    
#     sequence_length = 90
    
#     model = create_model(sequence_length)
#     model.load_weights('./models/weights/lstm_weights.h5')
    
#     input_data = scaled_data[-sequence_length:]
#     predicted_prices = predict_future(model, input_data, future_steps=15, scaler=scaler, sequence_length=sequence_length)
    
#     return predicted_prices.flatten().tolist()


def predict_btc_prices_from_api(sequence_length=90, future_steps=15):
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    
    df = get_data(start_date, end_date)
    if isinstance(df, int) and df == -1:
        raise ValueError("No data received from API")
    
    close_prices = df['Close'].values.tolist()
    print(sequence_length)
    close_prices = close_prices[-sequence_length:]
    
    btc_data = pd.DataFrame(close_prices, columns=['close'])
    # print("btc_data : ")
    # print(btc_data)
    
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(btc_data)
    
    model = create_model(sequence_length)
    model.load_weights('./models/weights/lstm_weights.h5')
    
    input_data = scaled_data[-sequence_length:]
    predicted_prices = predict_future(model, input_data, future_steps, scaler, sequence_length)
    print("pred : ",predicted_prices)

    return predicted_prices.flatten().tolist()


def simulation(sequence_length=90, future_steps=15, seed = 100, date = 1):
    end_date = datetime.now().strftime('%Y-%m-%d')

    if type(date) != int and date < 1:
        mins = date * 24 * 60
        start_date = (datetime.now() - timedelta(minutes=mins)).strftime('%Y-%m-%d')
    else:
        start_date = (datetime.now() - timedelta(days=date)).strftime('%Y-%m-%d')
    df = get_data(start_date, end_date)
    if isinstance(df, int) and df == -1:
        raise ValueError("No data received from API")
    
    close_prices = df['Close'].values
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(close_prices.reshape(-1, 1))
    
    model = create_model(sequence_length)
    model.load_weights('./models/weights/lstm_weights.h5')
    
    account = seed
    revenue_rate = 0.0
    days = 0
    print("start simulation || duration : ", (datetime.strptime(end_date, '%Y-%m-%d') - datetime.strptime(start_date, '%Y-%m-%d')).days, "|| window : ", sequence_length + future_steps)
    for i in range(len(scaled_data) - sequence_length - future_steps):
        input_data = scaled_data[i:i + sequence_length]
        predicted_prices = predict_future(model, input_data, future_steps, scaler, sequence_length)
        
        if predicted_prices[-1] > predicted_prices[0]:
            revenue_rate += (close_prices[i + sequence_length + future_steps - 1] - close_prices[i + sequence_length - 1]) / close_prices[i + sequence_length - 1]
            account = account * (1 + revenue_rate)

        if i % 1440 == 0:
            print(f"Progress Day {days} : {i}/{len(scaled_data) - sequence_length - future_steps}")
            days += 1

    output = {
        "init_seed" : seed,
        "final_seed" : account,
    }

    return output