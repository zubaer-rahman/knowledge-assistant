from app.services.chat.llm_service import LLMService
from app.services.chat.prompt_builder import PromptBuilder
from app.services.chat.chat_service import ChatService
from app.services.document.search_service import SearchService
from app.services.vector.vector_store import VectorStore


# Shared application state
vector_store = VectorStore()

# Services
search_service = SearchService(vector_store)
prompt_builder = PromptBuilder()
llm_service = LLMService()

chat_service = ChatService(
    search_service=search_service,
    prompt_builder=prompt_builder,
    llm_service=llm_service,
)


_vector_store = VectorStore()


def get_vector_store() -> VectorStore:
    return _vector_store


def get_search_service() -> SearchService:
    return SearchService(get_vector_store())


def get_prompt_builder() -> PromptBuilder:
    return prompt_builder


def get_llm_service() -> LLMService:
    return llm_service


def get_chat_service() -> ChatService:
    return chat_service