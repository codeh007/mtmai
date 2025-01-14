import os
import warnings
from typing import Annotated, Any, Literal

from pydantic import (AnyUrl, BeforeValidator, HttpUrl, computed_field,
                      model_validator)
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing_extensions import Self

from mtmlib import mtutils

from .__version__ import version


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    if isinstance(v, list | str):
        return v
    raise ValueError(v)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )
    app_name: str = "Mtmai API"
    PORT: int | None = 8000
    # admin_email: str | None = None
    items_per_user: int = 50
    # SECRET_KEY: str = secrets.token_urlsafe(32)
    SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"

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

    BACKEND_CORS_ORIGINS: Annotated[
        list[AnyUrl] | str, BeforeValidator(parse_cors)
    ] = []

    # db
    DATABASE_URL: str | None = None  # config("DATABASE_URL", cast=Secret)
    DATABASE_URL_2: str | None = None

    API_V1_STR: str = "/api/v1"
    VERSION: str | None = version

    vercel_token: str | None = None

    PROJECT_NAME: str = "mtmai"
    SENTRY_DSN: HttpUrl | None = None
    POSTGRES_SERVER: str = "POSTGRES_SERVER"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "POSTGRES_USER"
    POSTGRES_PASSWORD: str = ""
    POSTGRES_DB: str = ""

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

    # tembo
    TEMBO_TOKEN: str | None = None
    TEMBO_ORG: str | None = None
    TEMBO_INST: str | None = None
    TEMBO_DATA_DOMAIN: str | None = None

    # logging
    LOGGING_LEVEL: str | None = "info"
    LOGGING_PATH: str | None = ""
    LOGGING_FORMAT: str | None = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # cloudflared tunnel
    CF_TUNNEL_TOKEN: str | None = None
    CF_TUNNEL_TOKEN_TEMBO: str | None = None
    CF_TUNNEL_TOKEN_HF: str | None = None

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

    @model_validator(mode="after")
    def _enforce_non_default_secrets(self) -> Self:
        self._check_default_secret("SECRET_KEY", self.SECRET_KEY)
        self._check_default_secret("POSTGRES_PASSWORD", self.POSTGRES_PASSWORD)
        self._check_default_secret(
            "FIRST_SUPERUSER_PASSWORD", self.FIRST_SUPERUSER_PASSWORD
        )

        return self

    @computed_field  # type: ignore[prop-decorator]
    @property
    def is_in_gitpod(self) -> bool:
        return os.getenv("GITPOD_WORKSPACE_URL")

    @computed_field  # type: ignore[prop-decorator]
    @property
    def is_in_vercel(self) -> bool:
        return os.getenv("VERCEL")

    SEARXNG_URL_BASE: str | None = "http://127.0.0.1:18777"

    MAIN_GH_TOKEN: str | None = None
    MAIN_GH_USER: str | None = None

    DEFAULT_PASSWORD: str | None = "feihuo321"

    # huggingface
    HUGGINGFACEHUB_API_TOKEN: str | None = None
    HUGGINGFACEHUB_USER: str | None = None
    HUGGINGFACEHUB_DEFAULT_WORKSPACE: str | None = None

    gitsrc_dir: str | None = "gitsrc"

    IS_TRACE_HTTPX: bool = True
    OTEL_ENABLED: bool | None = False

    LOKI_ENDPOINT: str | None = "https://logs-prod-017.grafana.net/loki/api/v1/push"
    LOKI_USER: str | None = None
    GRAFANA_TOKEN: str | None = None

    # front
    # FRONT_PORT: int = 3800

    # POETRY_PYPI_TOKEN_PYPI: str | None = None

    MTMAI_API_BASE: str | None = None

    # storage
    @computed_field  # type: ignore[prop-decorator]
    @property
    def storage_dir(self) -> str:  # str | None = "/app/storage"
        if mtutils.is_in_gitpod() or mtutils.in_colab:
            return ".vol"

        return "/app/storage"


settings = Settings()  # type: ignore
