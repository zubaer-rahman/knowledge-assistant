from abc import ABC, abstractmethod
from pathlib import Path

from app.schemas.document import DocumentResponse


class BaseLoader(ABC):
    """Base class for all document loaders."""

    @abstractmethod
    def load(self, file_path: str | Path) -> DocumentResponse:
        """Load a document and return its contents."""
        raise NotImplementedError