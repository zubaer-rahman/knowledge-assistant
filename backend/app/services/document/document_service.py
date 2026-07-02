from app.schemas.chunk import Chunk
from app.schemas.document import DocumentResponse

from app.services.document.text_cleaner import TextCleaner
from app.services.document.chunker import TextChunker
from app.services.embedding.embedding_service import EmbeddingService
from app.services.vector.vector_store import VectorStore


class DocumentService:
    """
    Responsible for processing a document into searchable chunks.

    Pipeline:
        Document
            ↓
        Clean text
            ↓
        Chunk text
            ↓
        Generate embeddings
            ↓
        Store in FAISS
    """

    def __init__(self, vector_store: VectorStore):
        self.cleaner = TextCleaner()
        self.chunker = TextChunker()
        self.embedder = EmbeddingService()
        self.vector_store = vector_store

    def process(self, document: DocumentResponse) -> dict:
        all_chunks: list[Chunk] = []
        chunk_id = 0

        # Process each page independently
        for page_number, page_text in enumerate(document.pages, start=1):

            cleaned_text = self.cleaner.clean(page_text)

            page_chunks = self.chunker.chunk(cleaned_text)

            for text in page_chunks:
                all_chunks.append(
                    Chunk(
                        chunk_id=chunk_id,
                        source=document.filename,
                        page=page_number,
                        text=text,
                    )
                )
                chunk_id += 1

        if not all_chunks:
            return {
                "chunks": 0,
                "embedding_dim": 0,
            }

        # Generate embeddings
        texts = [chunk.text for chunk in all_chunks]

        embeddings = self.embedder.embed(texts)

        # Store in vector database
        self.vector_store.add(
            embeddings=embeddings,
            chunks=all_chunks,
        )

        print(f"Stored chunks: {len(all_chunks)}")
        print(
    f"Vectors in FAISS: "
    f"{self.vector_store.index.ntotal if self.vector_store.index else 0}"
)

        return {
            "chunks": len(all_chunks),
            "embedding_dim": len(embeddings[0]),
        }