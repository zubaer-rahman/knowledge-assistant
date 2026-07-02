from app.schemas.chunk import Chunk
from app.services.embedding.embedding_service import EmbeddingService
from app.services.vector.vector_store import VectorStore


class SearchService:
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store
        self.embedder = EmbeddingService()

    def search(self, query: str, k: int = 5) -> list[Chunk]:
        query_embedding = self.embedder.embed([query])[0]

        return self.vector_store.search(
            query_embedding,
            k,
        )