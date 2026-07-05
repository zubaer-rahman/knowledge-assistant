from app.services.chat.llm_service import LLMService
from app.services.chat.prompt_builder import PromptBuilder
from app.services.vector.vector_store import Chunk

builder = PromptBuilder()
llm = LLMService()

messages = builder.build(
    question="What is binary search?",
    chunks=[
        Chunk(
            chunk_id=1,
            source="book.pdf",
            page=1,
            text=(
                "Binary search is an algorithm that searches a "
                "sorted array by repeatedly dividing the search "
                "interval in half."
            ),
        )
    ],
)

answer = llm.generate(messages)

print(answer)