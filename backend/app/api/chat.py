from fastapi import APIRouter, HTTPException
from app.services.chat.chat_service import ChatService

router = APIRouter(prefix="/chat", tags=["Chat"])

service = ChatService()


@router.post("/")
async def chat(payload: dict):
    question = payload.get("question")
    if not question:
        raise HTTPException(status_code=400, detail="question is required")
    return await service.chat(question)