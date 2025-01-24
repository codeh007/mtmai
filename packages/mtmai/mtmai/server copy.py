import asyncio
import os
import threading
import uuid
from datetime import datetime
from typing import Awaitable, Callable

import structlog
import uvicorn
from dotenv import load_dotenv
from fastapi import APIRouter, Request
from fastapi.concurrency import asynccontextmanager
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute
from mtmai import analytics
from mtmai.app_forge import setup_forge_app
from mtmai.core import coreutils
from mtmai.core.__version__ import version
from mtmai.core.config import settings
from mtmai.core.coreutils import is_in_dev, is_in_vercel
from mtmai.exceptions import SkyvernHTTPException
from mtmai.forge.sdk.db.exceptions import NotFoundError
from mtmai.forge.sdk.settings_manager import SettingsManager
from mtmai.middleware import AuthMiddleware
from mtmaisdk.utils.env import is_in_docker, is_in_huggingface, is_in_windows
from mtmlib import mtutils
from pydantic import ValidationError
from starlette.requests import HTTPConnection
from starlette.requests import Request as StarletteRequest
from starlette.templating import Jinja2Templates
from starlette_context.plugins.base import Plugin

# from mtmai.workflows.workers import deploy_mtmai_workers

LOG = structlog.stdlib.get_logger()


class ExecutionDatePlugin(Plugin):
    key = "execution_date"

    async def process_request(
        self, request: StarletteRequest | HTTPConnection
    ) -> datetime:
        return datetime.now()


def build_app():
    from fastapi import FastAPI

    LOG.info("build api app.")

    LOG.info("api auth")
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

    # LOG.info("api agent")
    # from mtmai.api import agent

    # api_router.include_router(agent.router, prefix="/agent", tags=["agent"])

    LOG.info("api agent")
    from mtmai.api import agent

    api_router.include_router(agent.router, prefix="/agent", tags=["agent"])

    # LOG.info("api form")
    # from mtmai.api import form

    # api_router.include_router(form.router, prefix="/form", tags=["form"])

    LOG.info("api site")
    from mtmai.api import site

    api_router.include_router(site.router, prefix="/site", tags=["site"])

    LOG.info("api webpage")
    from mtmai.api import webpage

    api_router.include_router(webpage.router, prefix="/webpage", tags=["webpage"])

    LOG.info("api tasks")
    from mtmai.api import tasks

    api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])

    LOG.info("api openai")
    from mtmai.api import openai

    api_router.include_router(openai.router, tags=["openai"])

    LOG.info("api listview")
    from mtmai.api import listview

    api_router.include_router(listview.router, prefix="/listview", tags=["listview"])

    LOG.info("api workbench")
    from mtmai.api import workbench

    api_router.include_router(workbench.router, prefix="/workbench", tags=["workbench"])

    LOG.info("api logs")
    from mtmai.api import logs

    api_router.include_router(logs.router, prefix="/logs", tags=["logs"])

    LOG.info("api thread")
    from mtmai.api import thread

    api_router.include_router(thread.router, prefix="/thread", tags=["thread"])

    LOG.info("api artifact")
    from mtmai.api import artifact

    api_router.include_router(artifact.router, prefix="/artifact", tags=["artifact"])

    LOG.info("api config")
    from mtmai.api import config

    api_router.include_router(config.router, prefix="/config", tags=["config"])

    # LOG.info("api chat2")
    # from mtmai.api import chat2

    # api_router.include_router(chat2.router, prefix="/chat2", tags=["chat2"])

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        # deploy_mtmai_workers()
        yield
        # await taskWroker.stop()

    def custom_generate_unique_id(route: APIRoute) -> str:
        if len(route.tags) > 0:
            return f"{route.tags[0]}-{route.name}"
        return f"{route.name}"

    openapi_tags = [
        {
            "name": "admin",
            "description": "管理专用 ",
        },
        {
            "name": "train",
            "description": "模型训练及数据集",
        },
        {
            "name": "mtmcrawler",
            "description": "爬虫数据采集 ",
        },
        {
            "name": "openai",
            "description": "提供兼容 OPEN AI 协议 , 外置工作流 例如 langflow 可以通过此endpoint调用内部的工作流和模型",
        },
    ]

    app = FastAPI(
        # docs_url=None,
        # redoc_url=None,
        title=settings.PROJECT_NAME,
        description="mtmai description(group)",
        version=version,
        lifespan=lifespan,
        generate_unique_id_function=custom_generate_unique_id,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        swagger_ui_parameters={
            "syntaxHighlight": True,
            "syntaxHighlight.theme": "obsidian",
        },
        openapi_tags=openapi_tags,
    )
    templates = Jinja2Templates(directory="templates")

    if is_in_dev():
        from mtmai.api import admin

        api_router.include_router(
            admin.router,
            prefix="/admin",
            tags=["admin"],
        )
        # from mtmai.api import demos

        # api_router.include_router(
        #     demos.router, prefix="/demos/demos", tags=["demos_demos"]
        # )

    # app.openapi_schema = {
    #     "components": {
    #         "schemas": {
    #             "MessagePayload": MessagePayload.model_json_schema(),
    #             "AudioChunkPayload": AudioChunkPayload.model_json_schema(),
    #         }
    #     }
    # }

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):  # noqa: ARG001
        return JSONResponse(status_code=500, content={"detail": str(exc)})

    def setup_main_routes():
        from mtmai.api import home

        app.include_router(home.router)
        app.include_router(api_router, prefix=settings.API_V1_STR)

    setup_main_routes()

    if settings.OTEL_ENABLED:
        from mtmai.mtlibs import otel

        otel.setup_otel(app)

    if settings.BACKEND_CORS_ORIGINS:
        from fastapi.middleware.cors import CORSMiddleware

        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"]
            if settings.BACKEND_CORS_ORIGINS == "*"
            else [str(origin).strip("/") for origin in settings.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*", "x-chainlit-client-type"],
        )
        app.add_middleware(AuthMiddleware)

    setup_forge_app(app)

    from starlette_context.middleware import RawContextMiddleware

    app.add_middleware(
        RawContextMiddleware,
        plugins=(
            # TODO (suchintan): We should set these up
            ExecutionDatePlugin(),
            # RequestIdPlugin(),
            # UserAgentPlugin(),
        ),
    )

    from fastapi import FastAPI, Response, status

    @app.exception_handler(NotFoundError)
    async def handle_not_found_error(request: Request, exc: NotFoundError) -> Response:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    @app.exception_handler(SkyvernHTTPException)
    async def handle_skyvern_http_exception(
        request: Request, exc: SkyvernHTTPException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code, content={"detail": exc.message}
        )

    @app.exception_handler(ValidationError)
    async def handle_pydantic_validation_error(
        request: Request, exc: ValidationError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": str(exc)},
        )

    @app.exception_handler(Exception)
    async def unexpected_exception(request: Request, exc: Exception) -> JSONResponse:
        LOG.exception("Unexpected error in agent server.", exc_info=exc)
        return JSONResponse(
            status_code=500, content={"error": f"Unexpected error: {exc}"}
        )

    from mtmai.forge.sdk.core import skyvern_context
    from mtmai.forge.sdk.core.skyvern_context import SkyvernContext

    @app.middleware("http")
    async def request_middleware(
        request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        curr_ctx = skyvern_context.current()
        if not curr_ctx:
            request_id = str(uuid.uuid4())
            skyvern_context.set(SkyvernContext(request_id=request_id))
        elif not curr_ctx.request_id:
            curr_ctx.request_id = str(uuid.uuid4())

        try:
            return await call_next(request)
        finally:
            skyvern_context.reset()

    if SettingsManager.get_settings().ADDITIONAL_MODULES:
        for module in SettingsManager.get_settings().ADDITIONAL_MODULES:
            LOG.info("Loading additional module to set up api app", module=module)
            __import__(module)
        LOG.info(
            "Additional modules loaded to set up api app",
            modules=SettingsManager.get_settings().ADDITIONAL_MODULES,
        )

    from mtmai.forge import app as forge_app

    if forge_app.setup_api_app:
        forge_app.setup_api_app(app)

    return app


async def serve():
    try:
        analytics.capture("skyvern-oss-run-server")
        load_dotenv()

        app = build_app()
        # threading.Thread(target=start_deamon_serve).start()

        config = uvicorn.Config(
            app,
            host=settings.SERVE_IP,
            port=settings.PORT,
            log_level="info",
            # reload=not settings.is_production,
            # !!! bug 当 使用了prefect 后，使用了这个指令： @flow，程序会被卡在： .venv/lib/python3.12/site-packages/uvicorn/config.py
            # !!!365行：logging.config.dictConfig(self.log_config)
            # !!! 原因未知，但是 log_config=None 后，问题消失
            # log_config=None,
            # reload=reload,
        )

        host = (
            "127.0.0.1"
            if settings.SERVE_IP == "0.0.0.0"
            else settings.server_host.split("://")[-1]
        )
        server_url = f"{settings.server_host.split('://')[0]}://{host}:{settings.PORT}"

        LOG.info(
            "server config.", host="0.0.0.0", port=settings.PORT, server_url=server_url
        )
        server = uvicorn.Server(config)

        try:
            LOG.info(
                "server starting",
                host="0.0.0.0",
                port=settings.PORT,
                server_url=server_url,
            )
            await server.serve()
        except Exception as e:
            LOG.error("Error in uvicorn server:", exc_info=e)
            raise

    except Exception as e:
        LOG.error("server error: %s", e)


def start_deamon_serve():
    """
    启动后台独立服务
    根据具体环境自动启动
    """
    LOG.info("start_deamon_serve")
    if is_in_dev():
        from mtmai.flows.deployments import start_prefect_deployment

        start_prefect_deployment(asThreading=True)

    if (
        not settings.is_in_vercel
        and not settings.is_in_gitpod
        and settings.CF_TUNNEL_TOKEN
        and not is_in_huggingface()
        and not is_in_windows()
    ):
        from mtmlib import tunnel

        threading.Thread(target=lambda: asyncio.run(tunnel.start_cloudflared())).start()

        if not is_in_vercel() and not settings.is_in_gitpod:
            from mtmai.mtlibs.server.searxng import run_searxng_server

            threading.Thread(target=run_searxng_server).start()
        if (
            not settings.is_in_vercel
            and not settings.is_in_gitpod
            and not is_in_windows()
        ):

            def start_front_app():
                mtmai_url = coreutils.backend_url_base()
                if not mtutils.command_exists("mtmaiweb"):
                    LOG.warning("⚠️ mtmaiweb 命令未安装,跳过前端的启动")
                    return
                mtutils.bash(
                    f"PORT={settings.FRONT_PORT} MTMAI_API_BASE={mtmai_url} mtmaiweb serve"
                )

            threading.Thread(target=start_front_app).start()

            def start_prefect_server():
                LOG.info("启动 prefect server")

                sqlite_db_path = "/app/storage/prefect.db"
                sql_connect_str = f"sqlite+aiosqlite:///{sqlite_db_path}"
                mtutils.bash(
                    f"PREFECT_UI_STATIC_DIRECTORY=/app/storage PREFECT_API_DATABASE_CONNECTION_URL={sql_connect_str} prefect server start"
                )

            threading.Thread(target=start_prefect_server).start()

        if not is_in_vercel() and not settings.is_in_gitpod and not is_in_windows():
            from mtmai.mtlibs.server.kasmvnc import run_kasmvnc

            threading.Thread(target=run_kasmvnc).start()

        if is_in_docker():
            from mtmai.mtlibs.server.easyspider import run_easy_spider_server

            threading.Thread(target=run_easy_spider_server).start()

    LOG.info("start deamon finished")
