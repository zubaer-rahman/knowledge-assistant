import faiss
import numpy as np
from app.schemas.chunk import Chunk


class VectorStore:
    """Stores and retrieves document embeddings."""

    def __init__(self):
        self.index: faiss.Index | None = None
        self.chunks: list[Chunk] = []

    def add(self, embeddings, chunks: list[Chunk]) -> None:
        embeddings = np.asarray(embeddings, dtype="float32")

        if self.index is None:
            dimension = embeddings.shape[1]
            self.index = faiss.IndexFlatL2(dimension)

        self.index.add(embeddings)
        self.chunks.extend(chunks)

    def search(self, embedding, k: int = 5) -> list[Chunk]:
        if self.index is None:
            return []

        embedding = np.asarray([embedding], dtype="float32")

        _, indices = self.index.search(embedding, k)

        return [
    self.chunks[i]
    for i in indices[0]
    if i != -1
]