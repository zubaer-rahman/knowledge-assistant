from openai.types.chat import ChatCompletionAssistantMessageParam, ChatCompletionSystemMessageParam, ChatCompletionUserMessageParam

from app.schemas.chat import ChatMessage
from app.services.chat.types import ChatMessages
from app.services.vector.vector_store import Chunk


class PromptBuilder:
    """Builds prompts for Retrieval-Augmented Generation."""

    CONTEXT_SEPARATOR = "\n\n------------------------\n\n"

    SYSTEM_PROMPT = (
        "You are an AI assistant that answers questions using ONLY the provided "
        "document context.\n\n"
        "Rules:\n"
        "- Answer ONLY using the supplied context.\n"
        "- Do NOT use outside knowledge.\n"
        "- If the answer cannot be found in the context, reply exactly:\n"
        '  "I couldn\'t find that information in the uploaded document."\n'
        "- Do not invent facts.\n"
        "- Keep answers concise and accurate.\n"
        "- Summarize instead of copying large portions of the document.\n"
        "- Combine information from multiple context sections when needed.\n"
        "- Do not mention the context or document unless the user explicitly asks."
    )

    def _build_context(
        self,
        chunks: list[Chunk],
    ) -> str:
        context_parts: list[str] = []

        for chunk in chunks:
            context_parts.append(
                (
                    f"Source: {chunk.source}\n"
                    f"Page: {chunk.page}\n"
                    f"{chunk.text}"
                )
            )

        return self.CONTEXT_SEPARATOR.join(context_parts)

    def build(
        self,
        question: str,
        chunks: list[Chunk],
        history: list[ChatMessage],
    ) -> ChatMessages:
        context = self._build_context(chunks)

        user_prompt = (
            f"Context:\n\n"
            f"{context}\n\n"
            f"Question:\n"
            f"{question}\n\n"
            "Answer:"
        )

        messages: ChatMessages = [
            ChatCompletionSystemMessageParam(role="system", content=self.SYSTEM_PROMPT)
        ]

        for message in history:
            if message.role == "assistant":
                messages.append(
                    ChatCompletionAssistantMessageParam(role="assistant", content=message.content)
                )
            else:
                messages.append(
                    ChatCompletionUserMessageParam(role="user", content=message.content)
                )

        messages.append(
            ChatCompletionUserMessageParam(role="user", content=user_prompt)
        )

        # Temporary debugging (remove after verification)
        print("\n========== PROMPT SENT TO LLM ==========")

        for message in messages:
            print(f"\n[{message['role'].upper()}]")
            print(message["content"])

        print("\n========================================\n")

        return messages