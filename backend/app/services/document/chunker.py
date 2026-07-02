import re

from langchain_text_splitters import RecursiveCharacterTextSplitter


class TextChunker:
    """
    Splits text into overlapping chunks while preserving
    semantic boundaries and performs light cleanup on
    each resulting chunk.
    """

    def __init__(
        self,
        chunk_size: int = 800,
        chunk_overlap: int = 100,
    ):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=[
                "\n\n",
                "\n",
                ". ",
                "! ",
                "? ",
                "; ",
                ": ",
                ", ",
                " ",
                "",
            ],
        )

    def chunk(self, text: str) -> list[str]:
        chunks = self.splitter.split_text(text)

        cleaned_chunks = [
            self._clean_chunk(chunk)
            for chunk in chunks
            if chunk.strip()
        ]

        return cleaned_chunks

    @staticmethod
    def _clean_chunk(chunk: str) -> str:
        """Remove artifacts introduced during chunking."""
        chunk = chunk.strip()

        # Remove leading punctuation such as ".", ",", ";", etc.
        chunk = re.sub(r"^[^\w]+", "", chunk)

        # Normalize internal whitespace
        chunk = re.sub(r"\s+", " ", chunk)

        return chunk.strip()