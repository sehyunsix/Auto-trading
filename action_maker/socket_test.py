import websocket
import _thread
import time
import json
import logging

# 로그 설정
logging.basicConfig(filename='websocket.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# WebSocket에서 수신한 데이터를 저장할 리스트
received_data = []

def on_message(ws, message):
    global received_data
    data = json.loads(message)
    received_data.append(data)
    logging.info(f"Received message: {data}")

def on_error(ws, error):
    logging.error(f"Error: {error}")

def on_close(ws, close_status_code, close_msg):
    logging.info(f"### closed ### - Status code: {close_status_code}, Close message: {close_msg}")

def on_open(ws):
    logging.info("Opened connection")

def start_socket():
    websocket.enableTrace(False)  
    ws = websocket.WebSocketApp("wss://fstream.binance.com/stream?streams=bnbusdt@aggTrade/btcusdt@markPrice",
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.run_forever()

# WebSocket을 별도의 스레드에서 실행
_thread.start_new_thread(start_socket, ())