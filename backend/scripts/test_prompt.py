from app.services.chat.prompt_builder import PromptBuilder
from app.services.vector.vector_store import Chunk

builder = PromptBuilder()

messages = builder.build(
    question="What is binary search?",
    chunks=[
        Chunk(
            chunk_id=1,
            source="book.pdf",
            page=10,
            text="Binary search works on sorted arrays.",
        )
    ],
)

for message in messages:
    print(message)