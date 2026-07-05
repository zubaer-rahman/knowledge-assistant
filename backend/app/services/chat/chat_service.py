from app.schemas.chat import ChatResponse, SourceResponse
from app.services.chat.llm_service import LLMService
from app.services.chat.prompt_builder import PromptBuilder
from app.services.document.search_service import SearchService
from app.services.vector.vector_store import Chunk

class ChatService:
    def __init__(
        self,
        search_service: SearchService,
        prompt_builder: PromptBuilder,
        llm_service: LLMService,
    ):
        self.search_service = search_service
        self.prompt_builder = prompt_builder
        self.llm_service = llm_service

    def _generate_answer(
        self,
        question: str,
        chunks: list[Chunk],
    ) -> str:
        messages = self.prompt_builder.build(
            question=question,
            chunks=chunks,
        )
        return self.llm_service.generate(messages)

    def chat(self, question: str) -> ChatResponse:
        chunks = self.search_service.search(question, k=5)

        if not chunks:
            return ChatResponse(
                answer="I couldn't find any relevant information.",
                sources=[],
            )

        answer = self._generate_answer(
    question=question,
    chunks=chunks,
)

        return ChatResponse(
            answer=answer,
            sources=[
                SourceResponse(
                    source=chunk.source,
                    page=chunk.page,
                )
                for chunk in chunks
            ],
        )