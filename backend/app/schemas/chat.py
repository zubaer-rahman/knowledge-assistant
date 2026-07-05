from pydantic import BaseModel


class SourceResponse(BaseModel):
    source: str
    page: int


class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    answer: str
    sources: list[SourceResponse]