import sqlite3
from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine

from config import SQLITE_FILE_NAME

sqlite_url = f"sqlite:///{SQLITE_FILE_NAME}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables():
    """
    Create all tables stored in this metadata.

    Conditional by default, will not attempt to recreate tables already present in the target database.
    """
    SQLModel.metadata.create_all(engine)


def get_session():
    """
    Database session.
    """
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
