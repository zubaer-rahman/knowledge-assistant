from app.core.dependencies import vector_store
from app.services.document.search_service import SearchService
from app.services.llm.openrouter_client import OpenRouterClient


class ChatService:
    def __init__(self):
        self.search_service = SearchService(vector_store)
        self.llm = OpenRouterClient()

    async def chat(self, question: str):
        # 1. retrieve context
        chunks = self.search_service.search(question, k=5)

        context = "\n\n".join(f"[Source: {chunk.source}, Page: {chunk.page}]\n{chunk.text}" for chunk in chunks)

        # 2. generate answer
        answer = await self.llm.generate(question, context)

        return {
            "question": question,
            "context_used": chunks,
            "answer": answer,
        }