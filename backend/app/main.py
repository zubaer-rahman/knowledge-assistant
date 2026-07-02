from fastapi import FastAPI

from app.api.document import router as document_router

app = FastAPI(title="Personal Knowledge Assistant")

app.include_router(document_router)


@app.get("/")
def root():
    return {"message": "Knowledge Assistant API"}