from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
from pathlib import Path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, "../config/.env"))

app = {
    'name': 'mysql+pymysql',
    'user': os.environ["DB_ID"],
    'password': os.environ["DB_PW"],
    'host': os.environ["DB_HOST"],
    'dbconn': 'file_server',
    'port': os.environ["DB_PORT"],
}

conn_string = f'{app["name"]}://{app["user"]}:{app["password"]}@{app["host"]}:{app["port"]}/{app["dbconn"]}'


class Engine:

    def __init__(self):
        self.engine = create_engine(conn_string, pool_recycle=500)

    def sessionMaker(self):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        return session

    def connection(self):
        conn = self.engine.connect()
        return conn
