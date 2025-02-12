import os
import warnings
from pathlib import Path
from typing import Annotated, Any, Literal

from pydantic import AnyUrl, BeforeValidator, computed_field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing_extensions import Self

from .__version__ import version

APP_ROOT = os.getenv("MTMAI_APP_ROOT", os.getcwd())

HEADER_SITE_HOST = "X-Site-Host"  # 通过http header 传递前端域名


def parse_cors(v: Any) -> list[str] | str:
    if v == "*":
        return v
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )
    # 是否是生产环境
    is_production: bool = (
        os.environ.get("MTM_DEV", "development").lower() == "production"
    )
    app_name: str = "Mtmai"
    work_dir: str = os.getcwd()
    PORT: int = os.getenv("PORT", 7860)
    HOSTNAME: str | None = "0.0.0.0"  # noqa: S104
    SERVE_IP: str | None = "0.0.0.0"  # noqa: S104
    Serve_ADDR: str | None = None  # 明确指定服务器域名
    items_per_user: int = 50
    SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    COOKIE_ACCESS_TOKEN: str | None = "access_token"
    MEMBER_USER_DEFAULT_PASSWORD: str | None = "8888888@#@#123123"

    # oauth
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    DOMAIN: str = "localhost"
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"

    @computed_field  # type: ignore[prop-decorator]
    @property
    def server_host(self) -> str:
        # Use HTTPS for anything other than local development
        if self.ENVIRONMENT == "local":
            return f"http://{self.DOMAIN}"
        return f"https://{self.DOMAIN}"

    BACKEND_CORS_ORIGINS: Annotated[list[AnyUrl] | str, BeforeValidator(parse_cors)] = (
        "*"
    )

    # db
    MTMAI_DATABASE_URL: str | None = os.environ.get("MTMAI_DATABASE_URL", "development")

    API_V1_STR: str = "/api/v1"
    VERSION: str | None = version
    OPENAPI_JSON_PATH: str = "pyprojects/mtmai/mtmai/openapi.json"

    vercel_token: str | None = None

    PROJECT_NAME: str = "mtmai"
    SMTP_TLS: bool = True
    SMTP_SSL: bool = False
    SMTP_PORT: int = 587
    SMTP_HOST: str | None = None
    SMTP_USER: str | None = None
    SMTP_PASSWORD: str | None = None
    # TODO: update type to EmailStr when sqlmodel supports it
    EMAILS_FROM_EMAIL: str | None = None
    EMAILS_FROM_NAME: str | None = None

    # cloudflare
    CLOUDFLARE_ACCOUNT_ID: str | None = None
    CLOUDFLARE_API_EMAIL: str | None = None
    CLOUDFLARE_API_TOKEN: str | None = None
    CLOUDFLARE_AI_TOKEN: str | None = None

    # logging
    LOGGING_LEVEL: str | None = "info"
    LOGGING_PATH: str | None = ""
    LOGGING_FORMAT: str | None = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # cloudflared tunnel
    CF_TUNNEL_TOKEN: str | None = None
    CF_TUNNEL_TOKEN_TEMBO: str | None = None
    CF_TUNNEL_TOKEN_HF: str | None = None

    # storage
    @computed_field  # type: ignore[prop-decorator]
    @property
    def storage_dir(self) -> str:
        if Path(".vol").exists():
            return ".vol"
        return ".vol"

    @model_validator(mode="after")
    def _set_default_emails_from(self) -> Self:
        if not self.EMAILS_FROM_NAME:
            self.EMAILS_FROM_NAME = self.PROJECT_NAME
        return self

    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48

    @computed_field  # type: ignore[prop-decorator]
    @property
    def emails_enabled(self) -> bool:
        return bool(self.SMTP_HOST and self.EMAILS_FROM_EMAIL)

    EMAIL_TEST_USER: str = "test@example.com"
    FIRST_SUPERUSER: str = "mt@mt.com"
    FIRST_SUPERUSER_PASSWORD: str = "feihuo321"
    FIRST_SUPERUSER_EMAIL: str = "mt@mt.com"

    def _check_default_secret(self, var_name: str, value: str | None) -> None:
        if value == "changethis":
            message = (
                f'The value of {var_name} is "changethis", '
                "for security, please change it, at least for deployments."
            )
            if self.ENVIRONMENT == "local":
                warnings.warn(message, stacklevel=1)
            else:
                raise ValueError(message)

    # @model_validator(mode="after")
    # def _enforce_non_default_secrets(self) -> Self:
    #     self._check_default_secret("SECRET_KEY", self.SECRET_KEY)
    #     self._check_default_secret("POSTGRES_PASSWORD", self.POSTGRES_PASSWORD)
    #     self._check_default_secret(
    #         "FIRST_SUPERUSER_PASSWORD", self.FIRST_SUPERUSER_PASSWORD
    #     )

    #     return self

    # @computed_field  # type: ignore[prop-decorator]
    # @property
    # def is_in_gitpod(self) -> bool | None:
    #     return os.getenv("GITPOD_WORKSPACE_URL")

    @computed_field  # type: ignore[prop-decorator]
    @property
    def is_in_vercel(self) -> bool:
        return os.getenv("VERCEL")

    SEARXNG_URL_BASE: str | None = "http://127.0.0.1:18777"

    MAIN_GH_TOKEN: str | None = None
    MAIN_GH_USER: str | None = None

    GITHUB_CLIENT_ID: str | None = None
    GITHUB_CLIENT_SECRET: str | None = None

    # DEFAULT_PASSWORD: str | None = "feihuo321"

    # huggingface
    HUGGINGFACEHUB_API_TOKEN: str | None = None
    HUGGINGFACEHUB_USER: str | None = None
    HUGGINGFACEHUB_DEFAULT_WORKSPACE: str | None = None

    gitsrc_dir: str | None = "gitsrc"

    IS_TRACE_HTTPX: bool = True
    OTEL_ENABLED: bool | None = False

    # @property
    # def otel_deploy_name(self) -> str:
    #     if is_in_vercel():
    #         return "vercel"
    #     if mtutils.is_in_gitpod():
    #         return "gitpod"
    #     if is_in_huggingface():
    #         return "hf"
    #     return "unknown-deploy"

    LOKI_ENDPOINT: str | None = "https://logs-prod-017.grafana.net/loki/api/v1/push"
    LOKI_USER: str | None = None
    GRAFANA_TOKEN: str | None = None

    # front
    FRONT_PORT: int = 3800

    # POETRY_PYPI_TOKEN_PYPI: str | None = None

    # docker
    DOCKERHUB_PASSWORD: str | None = None
    DOCKERHUB_USER: str | None = None

    DOCKER_IMAGE_TAG: str | None = "docker.io/gitgit188/tmpboaiv3"

    # langgraph
    langgraph_checkpointer: Literal["memory", "postgres"] = "postgres"

    GROQ_TOKEN: str | None = ""
    TOGETHER_TOKEN: str | None = ""

    # http
    HTTP_PROXY: str | None = None
    HTTPS_PROXY: str | None = None
    # socks
    SOCKS_PROXY: str | None = None

    # https://serper.dev/api-key
    SERPER_DEV_TOKEN: str | None = None

    # selenium
    SELENIUM_VERSION: str = "4.24.0"
    SELENIUM_DISPLAY: str | None = None  # ":1"
    SELENIUM_PORT: int = 4444
    SELENIUM_HUB_URL: str | None = None

    # 其他
    graph_config_path: str = "configs/graph_config.yml"
    # mtforms_config_path: str = "configs/mtforms.yml"
    # chainlit
    CHAINLIT_AUTH_SECRET: str | None = None

    # prefect
    PREFECT_API_KEY: str | None = None
    PREFECT_API_URL: str | None = None

    WORKER_ENABLED: bool = True
    WORKER_NAME: str = "pyworker"
    WORKER_INTERVAL: int = 3
    WORKER_MAX_RETRY: int = 1000
    GOMTM_URL: str = "http://localhost:8383"
    HATCHET_CLIENT_TOKEN: str | None = None

    AG_HOST_ADDRESS: str = "0.0.0.0:7777"


settings = Settings()  # type: ignore
