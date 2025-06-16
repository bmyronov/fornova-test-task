import logging
import os
import json

from typing import Any

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, Response
from sqlmodel import select

from config import SCREENSHOT_DIR
from database import SessionDep
from producer import get_message
from models import Result

# Create a logger for the router module
logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/results")
def get_results(session: SessionDep) -> list[Result]:
    results = session.exec(select(Result)).all()

    return results


@router.get("/last_result")
def get_last_resilt(session: SessionDep) -> dict[Any, Any]:
    results = session.exec(select(Result)).all()

    if not results:
        return results

    result = results[-1].data

    return json.loads(result)


@router.get("/screenshot/{screenshot_name}")
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


def check_query(query) -> None:
    if not query:
        raise HTTPException(
            status_code=422, detail="You didn't specified any parameters"
        )

    key = [[k, v] for k, v in query.items()][0][0]
    if not key:
        raise HTTPException(
            status_code=422,
            detail="Can't process parameters. Parameters should be {hotel_name: date_list}",
        )

    key = [[k, v] for k, v in query.items()][0][0]
    if not isinstance(key, str):
        raise HTTPException(
            status_code=422,
            detail="Can't process parameters. hotel_name should be str",
        )

    value = [[k, v] for k, v in query.items()][0][1]
    if not isinstance(value, list):
        raise HTTPException(
            status_code=422,
            detail="Can't process parameters. date_list should be list",
        )


@router.post("/search")
def search_hotel(query: dict[str, list[list[str]]]):
    logger.info(f"Parameters: {query}")
    check_query(query)
    response = get_message(query)
    result: dict[str, Any] = json.loads(response)

    if not result:
        raise HTTPException(status_code=404, detail="Item not found")
    return result
