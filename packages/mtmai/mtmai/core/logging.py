import logging
import pathlib
from logging.handlers import RotatingFileHandler

from mtmai.core.config import settings
from mtmai.core.coreutils import is_in_dev

logs_dir = pathlib.Path(settings.storage_dir) / ".logs"


def get_logger(name: str | None = "root"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)  # 默认设置为 INFO 级别

    # 创建一个自定义的 StreamHandler
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)

    # 确保 logger 没有其他 handler
    logger.handlers = []
    logger.addHandler(handler)

    # 禁用 logger 的传播，以防止影响其他库的日志设置
    logger.propagate = False

    return logger


def setup_logging():
    log_format = (
        settings.LOGGING_FORMAT
        or "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    logging_level = settings.LOGGING_LEVEL.upper() or logging.INFO
    # print("logging level", logging_level)
    logging.basicConfig(
        level=logging_level,
        format=log_format,
        handlers=[
            logging.StreamHandler(),
        ],
    )

    root_logger = logging.getLogger()
    log_file = settings.LOGGING_PATH
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(root_logger.level)
        file_handler.setFormatter(logging.Formatter(log_format))
        root_logger.addHandler(file_handler)

    if settings.LOKI_ENDPOINT:
        print(
            f"use loki logging handler: {settings.LOKI_USER},{settings.LOKI_ENDPOINT}"
        )
        if not settings.GRAFANA_TOKEN:
            print("missing GRAFANA_TOKEN, skip setup loki")
        else:
            import logging_loki

            handler = logging_loki.LokiHandler(
                url=settings.LOKI_ENDPOINT,
                tags={
                    "application": settings.app_name,
                    "deploy": settings.otel_deploy_name,
                },
                auth=(settings.LOKI_USER, settings.GRAFANA_TOKEN),
                version="1",
            )
            root_logger.addHandler(handler)

    setup_root_logger()
    setup_sqlalchemy_logging()
    setup_httpx_logging()
    setup_openai_base_logging()


def setup_root_logger():
    root_logger = get_logger()
    root_logger.setLevel(logging.INFO)

    if is_in_dev():
        target_file = pathlib.Path(logs_dir) / "root.log"
        if not target_file.parent.exists():
            target_file.parent.mkdir(parents=True, exist_ok=True)

        file_handler = RotatingFileHandler(
            target_file, maxBytes=10 * 1024 * 1024, backupCount=5
        )
        file_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)


def setup_sqlalchemy_logging():
    sqlalchemy_logger = logging.getLogger("sqlalchemy.engine")
    sqlalchemy_logger.setLevel(logging.ERROR)
    print(f"SQLAlchemy logger level set to: {sqlalchemy_logger.level}")

    if is_in_dev():
        target_file = pathlib.Path(logs_dir) / "sqlalchemy.log"
        if not target_file.parent.exists():
            target_file.parent.mkdir(parents=True, exist_ok=True)

        file_handler = RotatingFileHandler(
            target_file, maxBytes=10 * 1024 * 1024, backupCount=5
        )
        file_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(formatter)
        sqlalchemy_logger.addHandler(file_handler)


def setup_httpx_logging():
    httpx_logger = logging.getLogger("httpx")
    httpx_logger.setLevel(logging.ERROR)
    print(f"httpx logger level set to: {httpx_logger.level}")

    if is_in_dev():
        target_file = pathlib.Path(logs_dir) / "httpx.log"

        if not target_file.parent.exists():
            target_file.parent.mkdir(parents=True, exist_ok=True)

        file_handler = RotatingFileHandler(
            target_file, maxBytes=10 * 1024 * 1024, backupCount=5
        )
        file_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(formatter)
        httpx_logger.addHandler(file_handler)


def setup_openai_base_logging():
    openai_base_client_logger = logging.getLogger("openai._base_client")
    openai_base_client_logger.setLevel(logging.ERROR)
    print(f"openai._base_client logger level set to: {openai_base_client_logger.level}")

    if is_in_dev():
        target_file = pathlib.Path(logs_dir) / "openai._base_client.log"

        if not target_file.parent.exists():
            target_file.parent.mkdir(parents=True, exist_ok=True)

        file_handler = RotatingFileHandler(
            target_file, maxBytes=10 * 1024 * 1024, backupCount=5
        )
        file_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(formatter)
        openai_base_client_logger.addHandler(file_handler)
