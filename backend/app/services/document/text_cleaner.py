import re


class TextCleaner:
    """Lightweight cleaning for transformer embeddings."""

    def clean(self, text: str) -> str:
        # Remove control characters
        text = re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F]", "", text)

        # Normalize Windows/Mac line endings
        text = text.replace("\r\n", "\n").replace("\r", "\n")

        # Collapse wrapped lines into spaces
        text = re.sub(r"(?<!\n)\n(?!\n)", " ", text)

        # Reduce multiple blank lines to one
        text = re.sub(r"\n{2,}", "\n\n", text)

        # Normalize spaces/tabs
        text = re.sub(r"[ \t]+", " ", text)

        return text.strip()