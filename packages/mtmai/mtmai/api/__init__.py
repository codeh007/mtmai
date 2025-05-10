from fastapi import APIRouter, FastAPI
from loguru import logger


def mount_api_routes(app: FastAPI, prefix=""):
    # api_router = APIRouter()

    # from mtmai.api import auth

    # api_router.include_router(auth.router, tags=["auth"])
    # logger.info("api auth")
    # from mtmai.api import chat

    # api_router.include_router(chat.router, tags=["chat"])
    # app.include_router(api_router, prefix=prefix)

    # app.include_router(api_router, prefix=prefix)

    # from mtmai.api import agent_runner

    # api_router.include_router(agent_runner.router, tags=["agent_runner"])
    # app.include_router(agent_runner.router, prefix=prefix, tags=["agent_runner"])

    from mtmai.api import tiktok_api

    # api_router.include_router(tiktok_api.router, tags=["tiktok_api"])
    app.include_router(tiktok_api.router, prefix=prefix, tags=["tiktok_api"])

    # from mtmai.api import video

    # api_router.include_router(llm.router, tags=["llm"])
    # api_router.include_router(video.router, tags=["video"])
    # app.include_router(api_router, prefix=prefix)
    from mtmai.api import tts

    app.include_router(tts.router, prefix=prefix, tags=["tts"])
