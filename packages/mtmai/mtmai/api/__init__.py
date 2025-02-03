from fastapi import APIRouter, FastAPI
from loguru import logger


def mount_api_routes(app: FastAPI, prefix=""):
    api_router = APIRouter()

    from mtmai.api import auth

    api_router.include_router(auth.router, tags=["auth"])
    # logger.info("api users")

    # from mtmai.api import users

    # api_router.include_router(users.router, prefix="/users", tags=["users"])

    logger.info("api chat")
    from mtmai.api import chat

    api_router.include_router(chat.router, tags=["chat"])

    # logger.info("api blog")
    # from mtmai.api import blog

    # api_router.include_router(blog.router, prefix="/posts", tags=["posts"])

    # logger.info("api image")
    # from mtmai.api import image

    # api_router.include_router(image.router, prefix="/image", tags=["image"])

    # logger.info("api train")
    # from mtmai.api import train

    # api_router.include_router(train.router, prefix="/train", tags=["train"])

    # logger.info("api metrics")
    # from mtmai.api import metrics

    # api_router.include_router(metrics.router, prefix="/metrics", tags=["metrics"])

    logger.info("api agent")
    from mtmai.api import agent

    api_router.include_router(agent.router, prefix="/agent", tags=["agent"])

    # logger.info("api predict")
    # from mtmai.api import predict

    # api_router.include_router(predict.router, prefix="/predict", tags=["predict"])

    logger.info("api sessions")
    from mtmai.api import sessions

    api_router.include_router(sessions.router, prefix="/sessions", tags=["sessions"])

    # logger.info("api agents")
    # from mtmai.api import agents

    # api_router.include_router(agents.router, prefix="/agents", tags=["agents"])

    # logger.info("api gallery")
    # from mtmai.api import gallery

    # api_router.include_router(gallery.router, prefix="/gallery", tags=["gallery"])

    logger.info("api teams")
    from mtmai.api import teams

    api_router.include_router(teams.router, prefix="/teams", tags=["teams"])

    logger.info("api runs")
    from mtmai.api import runs

    api_router.include_router(runs.router, prefix="/runs", tags=["runs"])

    logger.info("api ws")
    from mtmai.api import ws

    api_router.include_router(ws.router, prefix="/ws", tags=["ws"])

    # LOG.info("api form")
    # from mtmai.api import form

    # api_router.include_router(form.router, prefix="/form", tags=["form"])

    # LOG.info("api site")
    # from mtmai.api import site

    # api_router.include_router(site.router, prefix="/site", tags=["site"])

    # LOG.info("api webpage")
    # from mtmai.api import webpage

    # api_router.include_router(webpage.router, prefix="/webpage", tags=["webpage"])

    # LOG.info("api tasks")
    # from mtmai.api import tasks

    # api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])

    logger.info("api openai")
    from mtmai.api import openai

    api_router.include_router(openai.router, tags=["openai"])

    # LOG.info("api listview")
    # from mtmai.api import listview

    # api_router.include_router(listview.router, prefix="/listview", tags=["listview"])

    # LOG.info("api workbench")
    # from mtmai.api import workbench

    # api_router.include_router(workbench.router, prefix="/workbench", tags=["workbench"])

    # logger.info("api logs")
    # from mtmai.api import logs

    # api_router.include_router(logs.router, prefix="/logs", tags=["logs"])

    # LOG.info("api thread")
    # from mtmai.api import thread

    # api_router.include_router(thread.router, prefix="/thread", tags=["thread"])

    # LOG.info("api artifact")
    # from mtmai.api import artifact

    # api_router.include_router(artifact.router, prefix="/artifact", tags=["artifact"])

    logger.info("api config")
    from mtmai.api import config

    api_router.include_router(config.router, prefix="/config", tags=["config"])

    app.include_router(api_router, prefix=prefix)
