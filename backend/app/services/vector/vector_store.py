import faiss
import numpy as np
from app.schemas.chunk import Chunk
from app.services.document.search_result import SearchResult

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

    def search(self, embedding, k: int = 5) -> list[SearchResult]:
        if self.index is None:
            return []

        embedding = np.asarray([embedding], dtype="float32")

        distances, indices = self.index.search(embedding, k)

        results: list[SearchResult] = []

        for distance, index in zip(
            distances[0],
            indices[0],
        ):
            if index == -1:
                continue

            score = 1.0 / (1.0 + float(distance))

            results.append(
                SearchResult(
                    chunk=self.chunks[index],
                    score=score,
                )
            )

        return results