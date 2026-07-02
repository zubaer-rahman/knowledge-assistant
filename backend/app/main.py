from fastapi import FastAPI

from app.api.document import router as document_router
from app.api.search import router as search_router
from app.api.chat import router as chat_router

app = FastAPI(title="Personal Knowledge Assistant")

app.include_router(document_router)
app.include_router(search_router)
app.include_router(chat_router)


@app.get("/")
def root():
    return {"message": "Knowledge Assistant API"}