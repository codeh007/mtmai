import asyncio
import threading

from autogen_core import SingleThreadedAgentRuntime
import uvicorn
from fastapi import FastAPI, Request
from fastapi.concurrency import asynccontextmanager
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute
from loguru import logger

from mtmai.core.__version__ import version
from mtmai.core.config import settings
from mtmai.core.coreutils import is_in_dev, is_in_vercel
from mtmai.middleware import AuthMiddleware

from .worker import WorkerApp

from .api import mount_api_routes
from .utils.env import is_in_docker, is_in_huggingface, is_in_windows


def build_app():
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        # from mtmai.worker import WorkerAgent
        # worker_app = WorkerAgent()
        try:

            # worker_task = asyncio.create_task(worker_app.setup())

            yield
        except Exception as e:
            logger.exception(f"failed to setup worker: {e}")
        finally:
            # await worker_app.stop()
            # worker_task.cancel()
            # try:
            #     await worker_task
            # except asyncio.CancelledError:
            pass

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
    # templates = Jinja2Templates(directory="templates")

    # if is_in_dev():
    #     from mtmai.api import admin

    #     api_router.include_router(
    #         admin.router,
    #         prefix="/admin",
    #         tags=["admin"],
    #     )
    #     # from mtmai.api import demos

    #     # api_router.include_router(
    #     #     demos.router, prefix="/demos/demos", tags=["demos_demos"]
    #     # )

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

    def setup_main_routes(target_app: FastAPI):
        from mtmai.api import home

        target_app.include_router(home.router)
        # app.include_router(api_router, prefix=settings.API_V1_STR)
        mount_api_routes(target_app, prefix=settings.API_V1_STR)

    setup_main_routes(app)
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

    from .gradio_app import mount_gradio_app

    mount_gradio_app(app)

    # app.add_middleware(
    #     RawContextMiddleware,
    #     plugins=(
    #         # TODO (suchintan): We should set these up
    #         ExecutionDatePlugin(),
    #         # RequestIdPlugin(),
    #         # UserAgentPlugin(),
    #     ),
    # )

    # @app.exception_handler(NotFoundError)
    # async def handle_not_found_error(request: Request, exc: NotFoundError) -> Response:
    #     return Response(status_code=status.HTTP_404_NOT_FOUND)
    # @app.exception_handler(SkyvernHTTPException)
    # async def handle_skyvern_http_exception(
    #     request: Request, exc: SkyvernHTTPException
    # ) -> JSONResponse:
    #     return JSONResponse(
    #         status_code=exc.status_code, content={"detail": exc.message}
    #     )
    # @app.exception_handler(ValidationError)
    # async def handle_pydantic_validation_error(
    #     request: Request, exc: ValidationError
    # ) -> JSONResponse:
    #     return JSONResponse(
    #         status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    #         content={"detail": str(exc)},
    #     )
    # @app.exception_handler(Exception)
    # async def unexpected_exception(request: Request, exc: Exception) -> JSONResponse:
    #     LOG.exception("Unexpected error in agent server.", exc_info=exc)
    #     return JSONResponse(
    #         status_code=500, content={"error": f"Unexpected error: {exc}"}
    #     )
    # from mtmai.forge.sdk.core import skyvern_context
    # from mtmai.forge.sdk.core.skyvern_context import SkyvernContext
    # @app.middleware("http")
    # async def request_middleware(
    #     request: Request, call_next: Callable[[Request], Awaitable[Response]]
    # ) -> Response:
    # curr_ctx = skyvern_context.current()
    # if not curr_ctx:
    #     request_id = str(uuid.uuid4())
    #     skyvern_context.set(SkyvernContext(request_id=request_id))
    # elif not curr_ctx.request_id:
    #     curr_ctx.request_id = str(uuid.uuid4())
    # try:
    #     return await call_next(request)
    # finally:
    #     # skyvern_context.reset()
    #     pass
    # if SettingsManager.get_settings().ADDITIONAL_MODULES:
    #     for module in SettingsManager.get_settings().ADDITIONAL_MODULES:
    #         LOG.info("Loading additional module to set up api app", module=module)
    #         __import__(module)
    #     LOG.info(
    #         "Additional modules loaded to set up api app",
    #         modules=SettingsManager.get_settings().ADDITIONAL_MODULES,
    #     )
    # from mtmai.forge import app as forge_app
    # if forge_app.setup_api_app:
    #     forge_app.setup_api_app(app)
    return app


async def serve():
    await WorkerApp().run()
    app = build_app()
    config = uvicorn.Config(
        app,
        host=settings.SERVE_IP,
        port=settings.PORT,
        log_level="info",
    )

    host = (
        "127.0.0.1"
        if settings.SERVE_IP == "0.0.0.0"
        else settings.server_host.split("://")[-1]
    )
    server_url = f"{settings.server_host.split('://')[0]}://{host}:{settings.PORT}"

    logger.info(
        "server config.", host="0.0.0.0", port=settings.PORT, server_url=server_url
    )
    server = uvicorn.Server(config)

    try:
        logger.info(
            "server starting",
            host="0.0.0.0",
            port=settings.PORT,
            server_url=server_url,
        )
        await server.serve()
    except Exception as e:
        logger.error("Error in uvicorn server:", exc_info=e)
        raise

def start_deamon_serve():
    """
    启动后台独立服务
    根据具体环境自动启动
    """
    logger.info("start_deamon_serve")
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
        # from mtmlib import tunnel

        # threading.Thread(target=lambda: asyncio.run(tunnel.start_cloudflared())).start()

        if not is_in_vercel() and not settings.is_in_gitpod:
            from mtmai.mtlibs.server.searxng import run_searxng_server

            threading.Thread(target=run_searxng_server).start()
        if (
            not settings.is_in_vercel
            and not settings.is_in_gitpod
            and not is_in_windows()
        ):
            # def start_front_app():
            #     mtmai_url = coreutils.backend_url_base()
            #     if not mtutils.command_exists("mtmaiweb"):
            #         LOG.warning("⚠️ mtmaiweb 命令未安装,跳过前端的启动")
            #         return
            #     mtutils.bash(
            #         f"PORT={settings.FRONT_PORT} MTMAI_API_BASE={mtmai_url} mtmaiweb serve"
            #     )

            # threading.Thread(target=start_front_app).start()

            # def start_prefect_server():
            #     LOG.info("启动 prefect server")

            #     sqlite_db_path = "/app/storage/prefect.db"
            #     sql_connect_str = f"sqlite+aiosqlite:///{sqlite_db_path}"
            #     mtutils.bash(
            #         f"PREFECT_UI_STATIC_DIRECTORY=/app/storage PREFECT_API_DATABASE_CONNECTION_URL={sql_connect_str} prefect server start"
            #     )

            # threading.Thread(target=start_prefect_server).start()
            pass

        # if not is_in_vercel() and not settings.is_in_gitpod and not is_in_windows():
        #     from mtmai.mtlibs.server.kasmvnc import run_kasmvnc

        #     threading.Thread(target=run_kasmvnc).start()

        if is_in_docker():
            from mtmai.mtlibs.server.easyspider import run_easy_spider_server

            threading.Thread(target=run_easy_spider_server).start()

    # LOG.info("start deamon finished")
    # from mtmai.mtlibs.server.easyspider import run_easy_spider_server

    # threading.Thread(target=run_easy_spider_server).start()

    logger.info("start deamon finished")
