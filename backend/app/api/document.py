from pathlib import Path
import shutil

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.services.document.pdf_loader import PdfLoader

from app.core.dependencies import vector_store
from app.services.document.document_service import DocumentService

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)

UPLOAD_DIR = Path("app/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")

    destination = UPLOAD_DIR / file.filename

    with destination.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    loader = PdfLoader()
    document = loader.load(destination)

    service = DocumentService(vector_store)
    processing_result = service.process(document)

    return {
        "document": document,
        "processing": processing_result,
    }                   