import structlog
from fastapi import APIRouter, FastAPI

LOG = structlog.stdlib.get_logger()


def mount_api_routes(app: FastAPI, prefix="/"):
    api_router = APIRouter()

    from mtmai.api import auth

    api_router.include_router(auth.router, tags=["auth"])
    LOG.info("api users")

    from mtmai.api import users

    api_router.include_router(users.router, prefix="/users", tags=["users"])

    LOG.info("api blog")
    from mtmai.api import blog

    api_router.include_router(blog.router, prefix="/posts", tags=["posts"])

    LOG.info("api image")
    from mtmai.api import image

    api_router.include_router(image.router, prefix="/image", tags=["image"])

    LOG.info("api train")
    from mtmai.api import train

    api_router.include_router(train.router, prefix="/train", tags=["train"])

    LOG.info("api metrics")
    from mtmai.api import metrics

    api_router.include_router(metrics.router, prefix="/metrics", tags=["metrics"])

    LOG.info("api agent")
    from mtmai.api import agent

    api_router.include_router(agent.router, prefix="/agent", tags=["agent"])

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

    LOG.info("api openai")
    from mtmai.api import openai

    api_router.include_router(openai.router, tags=["openai"])

    # LOG.info("api listview")
    # from mtmai.api import listview

    # api_router.include_router(listview.router, prefix="/listview", tags=["listview"])

    # LOG.info("api workbench")
    # from mtmai.api import workbench

    # api_router.include_router(workbench.router, prefix="/workbench", tags=["workbench"])

    LOG.info("api logs")
    from mtmai.api import logs

    api_router.include_router(logs.router, prefix="/logs", tags=["logs"])

    # LOG.info("api thread")
    # from mtmai.api import thread

    # api_router.include_router(thread.router, prefix="/thread", tags=["thread"])

    # LOG.info("api artifact")
    # from mtmai.api import artifact

    # api_router.include_router(artifact.router, prefix="/artifact", tags=["artifact"])

    LOG.info("api config")
    from mtmai.api import config

    api_router.include_router(config.router, prefix="/config", tags=["config"])

    app.include_router(api_router, prefix=prefix)
