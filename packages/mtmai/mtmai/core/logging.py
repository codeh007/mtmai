import logging
import pathlib
from logging.handlers import RotatingFileHandler

from mtmai.core.config import settings

logs_dir = pathlib.Path(settings.storage_dir) / ".logs"


def get_logger(name: str | None = "root"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # 默认设置为 INFO 级别

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

    # if settings.LOKI_ENDPOINT:
    #     print(
    #         f"use loki logging handler: {settings.LOKI_USER},{settings.LOKI_ENDPOINT}"
    #     )
    #     if not settings.GRAFANA_TOKEN:
    #         print("missing GRAFANA_TOKEN, skip setup loki")
    #     else:
    #         import logging_loki

    #         handler = logging_loki.LokiHandler(
    #             url=settings.LOKI_ENDPOINT,
    #             tags={
    #                 "application": settings.app_name,
    #                 "deploy": settings.otel_deploy_name,
    #             },
    #             auth=(settings.LOKI_USER, settings.GRAFANA_TOKEN),
    #             version="1",
    #         )
    #         root_logger.addHandler(handler)

    root_logger = get_logger()
    root_logger.setLevel(logging.INFO)

    if settings.IS_DEV:
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
    setup_httpx_logging()


def setup_httpx_logging():
    httpx_logger = logging.getLogger("httpx")
    httpx_logger.setLevel(
        logging.WARNING
    )  # 将日志级别改为 WARNING，这样就不会显示 INFO 级别的日志

    target_file = pathlib.Path(logs_dir) / "httpx.log"
    print(f"httpx logger level set to: {httpx_logger.level}, logfile: {target_file}")

    if not target_file.parent.exists():
        target_file.parent.mkdir(parents=True, exist_ok=True)

    file_handler = RotatingFileHandler(
        target_file, maxBytes=10 * 1024 * 1024, backupCount=5
    )
    file_handler.setLevel(
        logging.DEBUG
    )  # 文件日志仍然保持 DEBUG 级别，以便需要时可以查看详细日志
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)
    httpx_logger.addHandler(file_handler)
