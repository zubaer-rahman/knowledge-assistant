from pathlib import Path

import fitz

from app.schemas.document import DocumentResponse


class PdfLoader:
    """Loads a PDF and extracts its text and metadata."""

    def load(self, file_path: str | Path) -> DocumentResponse:
        file_path = Path(file_path)

        pdf = fitz.open(file_path)

        pages: list[str] = []

        for page in pdf:
            pages.append(str(page.get_text()))

        document = DocumentResponse(
            filename=file_path.name,
            page_count=len(pdf),
            text="\n".join(pages),
            metadata=pdf.metadata or {},
        )

        pdf.close()

        return document