from pydantic import BaseModel


class Chunk(BaseModel):
    chunk_id: int
    source: str
    page: int
    text: str