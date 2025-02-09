from fastapi import APIRouter, FastAPI
from loguru import logger


def mount_api_routes(app: FastAPI, prefix=""):
    api_router = APIRouter()

    from mtmai.api import auth

    api_router.include_router(auth.router, tags=["auth"])
    logger.info("api chat")
    from mtmai.api import chat

    api_router.include_router(chat.router, tags=["chat"])
    app.include_router(api_router, prefix=prefix)
