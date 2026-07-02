from typing import Any

from pydantic import BaseModel


class DocumentResponse(BaseModel):
    filename: str
    page_count: int
    text: str
    metadata: dict[str, Any]