from fastapi import APIRouter
from fastapi import File
from fastapi import HTTPException, status, Depends, Request, Body
from bson import ObjectId
from typing import List
import base64
from models.inference import predict_btc_prices_from_api
from models.inference import simulation
# from socket_test import received_data
from fastapi import WebSocket, WebSocketDisconnect
import websockets
from datetime import datetime, timedelta
from schema.schemas import SimulationRequest

router = APIRouter()

@router.get("/action_make/api")
async def action_make_api():
    action_list = []
    try:
        pred = predict_btc_prices_from_api(sequence_length=90, future_steps=15)
        if pred[0] < pred[-1]:
            buy_action = {
                "index" : "0",
                "time" : datetime.now(),
                "params" : {
                    "symbol" : "BTCUSDT",
                    "side" : "BUY",
                    "type" : "STOP_LOSS",
                    "timeInForce" : "GTC",
                    "quantity" : "0.01",
                    "trailingDelta" : "500"
                }
            }
            sell_action = {
                "index" : "1",
                "time" : datetime.now()+timedelta(minutes=15),
                "params": {
                    "symbol": "BTCUSDT",
                    "side": "SELL",
                    "type": "STOP_LOSS",
                    "timeInForce": "GTC",
                    "quantity": "0.01",
                    "trailingDelta": "500",
                },
            }
            action_list.append(buy_action)
            action_list.append(sell_action)
        else:
            action_list = ["HOLD"]
        output = {
            "action_list": action_list,
            "prediction": pred
        }
        return output
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/simulation")
async def simulation_api(request: SimulationRequest = Body(...)):
    try:
        result = simulation(
            sequence_length=request.sequence_length,
            future_steps=request.future_steps,
            seed=request.seed,
            date=request.date
        )
        output = {
            "init_seed": result['init_seed'],
            "final_seed": result['final_seed'],
        }
        return output
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    

# @router.get("/action_make/socket")
# async def action_make():
#     action_list = []
#     try:
#         pred = predict_btc_prices_socket(received_data)
#         if pred[0] < pred[-1]:
#             buy_action = {
#                 "index" : "0",
#                 "time" : datetime.now(),
#                 "params" : {
#                     "symbol" : "BTCUSDT",
#                     "side" : "BUY",
#                     "type" : "STOP_LOSS",
#                     "timeInForce" : "GTC",
#                     "quantity" : "0.01",
#                     "trailingDelta" : "500"
#                 }
#             }
#             sell_action = {
#                 "index" : "1",
#                 "time" : datetime.now()+timedelta(minutes=15),
#                 "params": {
#                     "symbol": "BTCUSDT",
#                     "side": "SELL",
#                     "type": "STOP_LOSS",
#                     "timeInForce": "GTC",
#                     "quantity": "0.01",
#                     "trailingDelta": "500",
#                 },
#             }
#             action_list.append(buy_action)
#             action_list.append(sell_action)
#         else:
#             action_list = ["HOLD"]
#         output = {
#             "action_list": action_list,
#             "prediction": pred
#         }
#         return output
#     except ValueError as e:
#         raise HTTPException(status_code=400, detail=str(e))
