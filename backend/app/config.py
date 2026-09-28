import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()


class Settings:
    def __init__(self):
        self.DB_HOST = os.getenv("DB_HOST")
        self.DB_PORT = os.getenv("DB_PORT")
        self.DB_NAME = os.getenv("DB_NAME")
        self.DB_USER = os.getenv("DB_USER")
        self.DB_PWD = os.getenv("DB_PWD")

settings = Settings()
