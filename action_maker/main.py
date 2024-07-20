from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.route import router
from socket_test import start_socket
import _thread

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

# @app.on_event("startup")
# async def startup_event():
#     _thread.start_new_thread(start_socket, ())
