from app.services.chat.types import ChatMessages
from app.services.vector.vector_store import Chunk

class PromptBuilder:
    """Builds prompts for Retrieval-Augmented Generation."""

    SYSTEM_PROMPT = (
        "You are a helpful AI assistant.\n"
        "Answer ONLY using the provided context.\n"
        "If the answer cannot be found in the context, "
        "say you don't know.\n"
        "Do not make up facts."
    )

    def build(
        self,
        question: str,
        chunks: list[Chunk],
    ) -> ChatMessages:
        context = "\n\n".join(
            chunk.text
            for chunk in chunks
        )

        user_prompt = (
            f"Context:\n\n"
            f"{context}\n\n"
            f"Question:\n"
            f"{question}"
        )

        return [
            {
                "role": "system",
                "content": self.SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ]