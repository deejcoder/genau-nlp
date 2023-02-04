import logging
import traceback
from fastapi import FastAPI, Request, APIRouter
from fastapi.responses import JSONResponse
from tortoise import Tortoise

import config
from events import event, EventType
import database.models
import routes.transcribe


web_app = FastAPI()

# add routers here
router = APIRouter()
router.include_router(routes.transcribe.router)


# include all routers in the web_app
web_app.include_router(router)


@web_app.exception_handler(Exception)
async def internal_server_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": f"Oops, an error has occurred! {traceback.format_exc()}"}
    )


@web_app.on_event("startup")
async def init() -> None:
    database.models.load_models()

    await Tortoise.init(
        db_url=config.CONNECTION_STRING,
        modules={"models": ["database.models"]},
    )

    logging.info("Tortoise-ORM started, generating schemas...")
    await Tortoise.generate_schemas()
    logging.info("Generated schemas.")
    logging.info("Running post-generation scripts...")

    await event.emit_async(EventType.Index.post_schema_generation)
    logging.info("Database initialized.")


@web_app.on_event("shutdown")
async def close() -> None:
    await Tortoise.close_connections()
    logging.info("Database connection closed.")

