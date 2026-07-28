from pydantic import BaseModel, Field


class SourceResponse(BaseModel):
    source: str
    page: int

class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    question: str
    history: list[ChatMessage] = Field(default_factory=list)


class ChatResponse(BaseModel):
    answer: str
    sources: list[SourceResponse]