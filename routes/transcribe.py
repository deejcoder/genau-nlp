from pathlib import Path

from fastapi import UploadFile, APIRouter
from fastapi.responses import JSONResponse
from typing import Optional

import config
from services import FileUploader
from services.transcriber import transcriber


router = APIRouter(
    prefix="/transcribe",
    tags=["transcribe"],
    responses={404: {"description": "Not Found"}}
)


@router.post("/upload")
async def upload_file(file: UploadFile, language: Optional[str] = None):
    manager = FileUploader()
    file_path = await manager.save_file(file, Path(config.UPLOAD_FILE_PATH))

    result = transcriber.transcribe_from_file(file_path, language)

    return JSONResponse(
        status_code=200,
        content={
            "language": result.language,
            "text": result.text
        }
    )
