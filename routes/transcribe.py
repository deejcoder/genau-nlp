from pathlib import Path

from fastapi import UploadFile, APIRouter
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from typing import Optional

import config
from services import FileUploader
from services.transcriber import transcriber, TranscribeResult


router = APIRouter(
    prefix="/transcribe",
    tags=["transcribe"],
    responses={404: {"description": "Not Found"}},
)


class TranscribeResponse(BaseModel):
    language: str
    text: str


@router.post("/upload", response_model=TranscribeResponse)
async def upload_file(file: UploadFile, language: Optional[str] = None) -> TranscribeResponse:
    manager = FileUploader()
    file_path = await manager.save_file(file, Path(config.UPLOAD_FILE_PATH))

    result = transcriber.transcribe_from_file(file_path, language)

    return TranscribeResponse(language=result.language, text=result.text)

