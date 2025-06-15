import os
import logging
import json

from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, Response
from sqlmodel import select, Session

from config import SCREENSHOT_DIR
from producer import get_message
from database import SessionDep, create_db_and_tables
from models import Result
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
