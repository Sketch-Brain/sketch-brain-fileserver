from fastapi import FastAPI
import os
from fastapi.middleware.cors import CORSMiddleware
import time
import logging
from dotenv import load_dotenv

from log_conf import log_config
from logging.config import dictConfig
from router import file_mgr

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, "./config/.env"))
dictConfig(log_config)
logger = logging.getLogger("fileserver-logger")

app = FastAPI()

app.include_router(file_mgr.router)
