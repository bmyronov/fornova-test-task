import os
import logging
import json

from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, Response
from sqlmodel import select, Session
from pika import ConnectionParameters

from config import SCREENSHOT_DIR
from producer import get_message
from database import SessionDep, create_db_and_tables, engine
from models import Result

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


@app.get("/results")
def get_results(session: SessionDep) -> list[Result]:
    results = session.exec(select(Result)).all()

    return results


@app.get("/last_result")
def get_last_resilt(session: SessionDep) -> dict[Any, Any]:
    results = session.exec(select(Result)).all()

    if not results:
        return results

    result = results[-1].data

    return json.loads(result)


@app.get("/screenshot/{screenshot_name}")
def get_screenshot(screenshot_name: str) -> Response:
    # Creates screenshot folder if it doesn't exists
    if not os.path.isdir(SCREENSHOT_DIR):
        logger.warning("Screenshot folder does not exists!")

        os.makedirs(SCREENSHOT_DIR)
        logger.info("Screenshot directory has been created!")

    file_path: str = SCREENSHOT_DIR + "/" + screenshot_name
    # If file doesn't exists return error 404
    if not os.path.exists(file_path):
        logger.info(f"{screenshot_name} does not exists")
        raise HTTPException(status_code=404, detail="Item not found")

    # If you would like to download the image, instead of just opening it, use this method
    # return FileResponse(file_path, filename=screenshot_name, media_type="image/png")

    with open(file_path, "rb") as f:
        image_bytes = f.read()
    return Response(content=image_bytes, media_type="image/png")


@app.get("/test")
def test():
    return {"url": "http://localhost:8000/screenshot/1.png"}


@app.post("/search")
def search_hotel(query: dict[str, list[list[str]]]):
    logger.info(f"Parameters: {query}")
    response = get_message(query)
    result: dict[str, Any] = json.loads(response)

    if not result:
        raise HTTPException(status_code=404, detail="Item not found")
    return result
