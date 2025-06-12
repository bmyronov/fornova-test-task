from sqlmodel import Field, Session, SQLModel


class Result(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    data: str
