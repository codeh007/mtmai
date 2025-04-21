from fastapi import APIRouter, FastAPI
from loguru import logger


def mount_api_routes(app: FastAPI, prefix=""):
    api_router = APIRouter()

    # from mtmai.api import auth

    # api_router.include_router(auth.router, tags=["auth"])
    # logger.info("api auth")
    # from mtmai.api import chat

    # api_router.include_router(chat.router, tags=["chat"])
    # app.include_router(api_router, prefix=prefix)

    from mtmai.api import browser_use

    api_router.include_router(browser_use.router, tags=["browser_use"])
    app.include_router(api_router, prefix=prefix)

    from mtmai.api import agent_runner

    api_router.include_router(agent_runner.router, tags=["smolagent"])
    app.include_router(api_router, prefix=prefix)

    from mtmai.api import dev_ui

    dev_ui.configure_dev_web_ui(app)
