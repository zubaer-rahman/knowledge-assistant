from dataclasses import dataclass

from app.services.vector.vector_store import Chunk


@dataclass(slots=True)
class SearchResult:
    chunk: Chunk
    score: float