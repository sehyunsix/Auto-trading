from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel

class SimulationRequest(BaseModel):
    sequence_length: int
    future_steps: int
    seed: int
    date: float