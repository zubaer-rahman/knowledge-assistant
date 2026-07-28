from app.schemas.chat import ChatMessage
from app.core.config import settings
from app.schemas.chat import ChatResponse, SourceResponse
from app.services.chat.llm_service import LLMService
from app.services.chat.prompt_builder import PromptBuilder
from app.services.document.search_result import SearchResult
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
        self.min_search_score = settings.MIN_SEARCH_SCORE

    def _get_chunks(
        self,
        results: list[SearchResult],
    ) -> list[Chunk]:
        return [
            result.chunk
            for result in results
        ]

    def _get_sources(
        self,
        results: list[SearchResult],
    ) -> list[SourceResponse]:
        seen: set[tuple[str, int]] = set()
        sources: list[SourceResponse] = []

        for result in results:
            key = (
                result.chunk.source,
                result.chunk.page,
            )

            if key in seen:
                continue

            seen.add(key)

            sources.append(
            SourceResponse(
                source=result.chunk.source,
                page=result.chunk.page,
            )
        )

        return sources

    def _filter_results(
        self,
        results: list[SearchResult],
    ) -> list[SearchResult]:
        return [
            result
            for result in results
            if result.score >= self.min_search_score
        ]
        
    def _generate_answer(
        self,
        question: str,
        chunks: list[Chunk],
        history: list[ChatMessage],
    ) -> str:
        messages = self.prompt_builder.build(
            question=question,
            chunks=chunks,
            history=history,
        )

        return self.llm_service.generate(messages)

    def chat(
        self,
        question: str,
        history: list[ChatMessage],
    ) -> ChatResponse:
        results = self.search_service.search(
            question,
            k=5,
        )
        results = self._filter_results(results)

        if not results:
            return ChatResponse(
                answer="I couldn't find any relevant information.",
                sources=[],
            )

        chunks = self._get_chunks(results)

        answer = self._generate_answer(
            question=question,
            chunks=chunks,
            history=history,
        )

        return ChatResponse(
            answer=answer,
            sources=self._get_sources(results),
        )