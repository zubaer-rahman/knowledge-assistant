from typing import Any

from pydantic import BaseModel


class DocumentResponse(BaseModel):
    filename: str
    page_count: int
    pages: list[str]
    metadata: dict[str, Any]