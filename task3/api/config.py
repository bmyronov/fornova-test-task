import os
from dotenv import load_dotenv

load_dotenv()

RABBITMQ_HOST: str = os.environ.get("RABBITMQ_HOST")
RABBITMQ_PORT: str = os.environ.get("RABBITMQ_PORT")

SQLITE_FILE_NAME = "database.db"
SCREENSHOT_DIR = "../screenshots"
