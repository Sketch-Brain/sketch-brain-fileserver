from fastapi import FastAPI
import os
from fastapi.middleware.cors import CORSMiddleware
import time
import logging

from log_conf import log_config
from logging.config import dictConfig
from router import file_mgr
dictConfig(log_config)
logger = logging.getLogger("fileserver-logger")

app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(file_mgr.router)