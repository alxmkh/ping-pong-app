from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import api

origins = [
    "http://localhost:4001/ping-pong",
    "localhost:4001/ping-pong",
    "http://0.0.0.0:4001/ping-pong",
    "0.0.0.0:4001/ping-pong"
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(api.router)

