import inspect
import logging
from inspect import getmembers
from pathlib import Path

import uvicorn
import traceback
from fastapi import FastAPI, UploadFile, Request
from fastapi.responses import JSONResponse
from tortoise import Tortoise, run_async
from tortoise.contrib.fastapi import register_tortoise

import config
import database.models
from database.models import BaseModel
from services import FileUploader, Transcriber

app = FastAPI()

# init the transcriber when the api starts, as loading the model can take time
transcriber = Transcriber()


@app.exception_handler(Exception)
async def internal_server_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": f"Oops, an error has occurred! {traceback.format_exc()}"}
    )


@app.post("/upload")
async def upload_file(file: UploadFile):
    manager = FileUploader()
    file_path = await manager.save_file(file, Path(config.UPLOAD_FILE_PATH))

    result = transcriber.transcribe_from_file(file_path)

    return JSONResponse(
        status_code=200,
        content={
            "language": result.language,
            "text": result.text
        }
    )


async def exec_post_generation_scripts():
    models = [m[1] for m in getmembers(database.models) if inspect.isclass(m[1]) and issubclass(m[1], BaseModel)]
    for model in models:
        if hasattr(model, 'on_post_generate'):
            method = getattr(model, 'on_post_generate')
            if callable(method) and inspect.iscoroutinefunction(method):
                await method()


@app.on_event("startup")
async def init() -> None:
    await Tortoise.init(
        db_url=config.CONNECTION_STRING,
        modules={"models": ["database.models"]},
    )

    logging.info("Tortoise-ORM started, generating schemas...")
    await Tortoise.generate_schemas()
    logging.info("Generated schemas.")
    logging.info("Running post-generation scripts...")
    await exec_post_generation_scripts()
    logging.info("Database initialized.")


@app.on_event("shutdown")
async def close() -> None:
    await Tortoise.close_connections()
    logging.info("Database connection closed.")


uvicorn.run(app, host="0.0.0.0", port=8000)



