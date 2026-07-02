from fastapi import APIRouter
from app.core.dependencies import vector_store
from app.services.document.search_service import SearchService

router = APIRouter(prefix="/search", tags=["Search"])

service = SearchService(vector_store)


@router.get("/")
def search(q: str):
    return {
        "query": q,
        "results": service.search(q)
    }