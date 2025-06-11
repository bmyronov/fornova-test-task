from pydantic import BaseModel


class SearchResult(BaseModel):
    index: int
    type: str
    name: str
