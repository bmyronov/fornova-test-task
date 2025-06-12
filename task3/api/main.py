import logging
import json

from typing import Any

from fastapi import FastAPI, HTTPException
from sqlmodel import select, Session
from pika import ConnectionParameters

from config import RABBITMQ_HOST, RABBITMQ_PORT
from producer import HotelResult
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
connection_params = ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT)


def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)


def get_message(query: str) -> str:
    hotel_result = HotelResult(connection_params=connection_params)
    response: str | None = hotel_result.call(query)

    return response


def create_result(data: Any) -> None:
    session = Session(engine)
    result = Result(id=None, data=data)

    session.add(result)
    print(session)
    session.commit()
    session.refresh(result)


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


@app.get("/search")
def search_hotel():
    hotel_name: str = "The Grosvenor Hotel"
    date_list: list[list[str]] = [
        ["June 15", "June 16"],
        ["June 16", "June 17"],
        ["June 17", "June 18"],
        ["June 18", "June 19"],
        ["June 19", "June 26"],
    ]
    query = {hotel_name: date_list}

    response = get_message(json.dumps(query))
    result = json.loads(response)
    # Add result to db
    create_result(response)

    if not result:
        raise HTTPException(status_code=404, detail="Item not found")
    return result
