from typing import Any

from sqlmodel import Session

from database import engine
from models import Result


def create_result(data: Any) -> None:
    session = Session(engine)
    result = Result(data=data)

    session.add(result)
    session.commit()
    session.refresh(result)
