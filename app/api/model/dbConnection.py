from sqlalchemy import create_engine
from urllib.parse import quote
from dotenv import load_dotenv

import os
load_dotenv()

USER = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")
HOST = os.getenv("DB_HOST")
PORT = os.getenv("DB_PORT")
DATABASE = os.getenv("DB_DATABASE")

def get_connection():
    return create_engine(
        url="mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(
            USER, quote(PASSWORD), HOST, PORT, DATABASE
        )
    )