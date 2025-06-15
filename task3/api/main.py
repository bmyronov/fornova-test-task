import logging

from fastapi import FastAPI
from database import create_db_and_tables
from routers import router

# Configure logging
logger = logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%d-%m-%Y %H:%M:%S",
    # filename="./logs/basic.log",
)

# Create a logger for the main module
logger = logging.getLogger(__name__)


def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router=router)
