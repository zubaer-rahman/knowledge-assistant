from pathlib import Path

import fitz  # PyMuPDF

from app.schemas.document import DocumentResponse


class PdfLoader:
    """
    Responsible only for extracting text and metadata from PDF files.

    Design goals:
    - Safe file handling
    - Clean text extraction
    - Compatible with RAG pipeline (chunking + embeddings)
    """

    def load(self, file_path: str | Path) -> DocumentResponse:
        file_path = Path(file_path)

        # Safe context manager ensures file is always closed properly
        with fitz.open(file_path) as pdf:

            # Extract text from all pages
            pages = [str(page.get_text("text")).strip() for page in pdf]

            # Build structured response
            return DocumentResponse(
                filename=file_path.name,
                page_count=len(pdf),
                pages=pages,
                metadata=pdf.metadata or {},
            )   