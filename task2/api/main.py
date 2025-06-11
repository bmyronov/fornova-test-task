import json

import httpx
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder

from config import TEST_RUNNER_URL

app = FastAPI()


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
    data = {hotel_name: date_list}

    response = httpx.post(
        f"{TEST_RUNNER_URL}/search", data=json.dumps(data), timeout=None
    )
    if response.status_code == 200:
        return response.json()  # or process the response as needed
    else:
        return {"error": f"Request failed with status code: {response.status_code}"}
