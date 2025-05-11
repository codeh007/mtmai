import os
import warnings
from pathlib import Path
from typing import Annotated, Any, Literal

from pydantic import AnyUrl, BeforeValidator, computed_field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing_extensions import Self


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
    PORT: int = os.getenv("PORT", 7861)
    HOSTNAME: str | None = "0.0.0.0"  # noqa: S104
    SERVE_IP: str | None = "0.0.0.0"  # noqa: S104
    Serve_ADDR: str | None = None  # 明确指定服务器域名
    items_per_user: int = 50
    SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    COOKIE_ACCESS_TOKEN: str | None = "access_token"
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
    MTM_DATABASE_URL: str | None = os.environ.get("MTM_DATABASE_URL", "development")

    API_PREFIX: str = "/api/mtmai"
    # OPENAPI_JSON_PATH: str = "pyprojects/mtmai/mtmai/openapi.json"

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
    # CLOUDFLARE_ACCOUNT_ID: str | None = None
    # CLOUDFLARE_API_EMAIL: str | None = None
    # CLOUDFLARE_API_TOKEN: str | None = None
    # CLOUDFLARE_AI_TOKEN: str | None = None

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

    # @computed_field  # type: ignore[prop-decorator]
    # @property
    # def is_in_vercel(self) -> bool:
    #     return os.getenv("VERCEL")

    SEARXNG_URL_BASE: str | None = "http://127.0.0.1:18777"

    MAIN_GH_TOKEN: str | None = None
    MAIN_GH_USER: str | None = None

    GITHUB_CLIENT_ID: str | None = None
    GITHUB_CLIENT_SECRET: str | None = None

    # huggingface
    HUGGINGFACEHUB_API_TOKEN: str | None = None
    HUGGINGFACEHUB_USER: str | None = None
    HUGGINGFACEHUB_DEFAULT_WORKSPACE: str | None = None

    # gitsrc_dir: str | None = "gitsrc"

    IS_TRACE_HTTPX: bool = True
    OTEL_ENABLED: bool | None = False
    LOKI_ENDPOINT: str | None = "https://logs-prod-017.grafana.net/loki/api/v1/push"
    LOKI_USER: str | None = None
    GRAFANA_TOKEN: str | None = None

    # front
    # FRONT_PORT: int = 3800

    # POETRY_PYPI_TOKEN_PYPI: str | None = None

    # docker
    DOCKERHUB_PASSWORD: str | None = None
    DOCKERHUB_USER: str | None = None

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

    # prefect
    PREFECT_API_KEY: str | None = None
    PREFECT_API_URL: str | None = None

    WORKER_ENABLED: bool = True
    WORKER_NAME: str = "pyworker"
    WORKER_INTERVAL: int = 3
    WORKER_MAX_RETRY: int = 1000
    GOMTM_URL: str = "http://127.0.0.1:8383"
    # AG_HOST_ADDRESS: str = "0.0.0.0:7777"
    DEFAULT_CLIENT_TIMEOUT: int = 20
    GOMTM_API_PATH_PREFIX: str = "/mtmapi"

    # OPENAI
    OPENAI_API_KEY: str | None = os.environ.get("OPENAI_API_KEY", "openai_key_not_set")
    OPENAI_BASE_URL: str | None = os.environ.get(
        "OPENAI_BASE_URL", "openai_base_url_not_set"
    )

    @property
    def NVIDIA_API_KEY(self) -> str | None:
        return os.environ.get("NVIDIA_API_KEY", "nvidia_api_key_not_set")

    @property
    def OPENROUTER_API_KEY(self) -> str | None:
        return os.environ.get("OPENROUTER_API_KEY", "openrouter_api_key_not_set")

    @property
    def WEATHER_API_KEY(self) -> str | None:
        return os.environ.get("WEATHER_API_KEY", "weather_api_key_not_set")

    @property
    def GOOGLE_AI_STUDIO_API_KEY(self) -> str | None:
        return os.environ.get("GEMINI_API_KEY", "google_ai_studio_api_key_not_set")

    @property
    def GOOGLE_AI_STUDIO_API_KEY_2(self) -> str | None:
        return os.environ.get(
            "GOOGLE_AI_STUDIO_API_KEY_2", "google_ai_studio_api_key_not_set"
        )

    @property
    def HF_TOKEN(self) -> str | None:
        return os.environ.get("HF_TOKEN", "nvidia_api_key_not_set")

    default_proxy_url: str = "http://127.0.0.1:10809"

    @property
    def BROWSER_DEBUG_PORT(self) -> int:
        return os.environ.get("BROWSER_DEBUG_PORT", 19222)

    @property
    def JINA_API_KEY(self) -> str | None:
        return os.environ.get("JINA_API_KEY", "jina_api_key_not_set")

    @property
    def SERPAPI_API_KEY(self) -> str | None:
        return os.environ.get("SERPAPI_API_KEY", "serpapi_api_key_not_set")

    @property
    def AGENT_DIR(self) -> str | None:
        return os.environ.get("MTM_AGENT_DIR", "./mtmai/agents")

    @property
    def WORKER_GATEWAY_URL(self) -> str | None:
        return os.environ.get("WORKER_GATEWAY_URL", "https://mtmag.yuepa8.com")

    @property
    def PEXELS_API_KEYS(self) -> list[str]:
        return os.environ.get("PEXELS_API_KEYS", "pexels_api_key_not_set").split(",")

    @property
    def CLOUDFLARE_R2_ENDPOINT(self) -> str | None:
        return os.environ.get(
            "CLOUDFLARE_R2_ENDPOINT", "cloudflare_r2_endpoint_not_set"
        )

    @property
    def CLOUDFLARE_R2_ACCESS_KEY(self) -> str | None:
        return os.environ.get(
            "CLOUDFLARE_R2_ACCESS_KEY", "cloudflare_r2_access_key_not_set"
        )

    @property
    def CLOUDFLARE_R2_SECRET_KEY(self) -> str | None:
        return os.environ.get(
            "CLOUDFLARE_R2_SECRET_KEY", "cloudflare_r2_secret_key_not_set"
        )

    @property
    def CLOUDFLARE_R2_BUCKET(self) -> str | None:
        return os.environ.get("CLOUDFLARE_R2_BUCKET", "default")

    @property
    def DEMO_USER_ID(self) -> str | None:
        """
        默认用户id
        """
        return os.environ.get("DEMO_USER_ID", "076293cb-7f2c-4844-a178-ebe299f77034")

    @property
    def QUEUE_SHORTVIDEO_COMBINE(self) -> str | None:
        return os.environ.get("QUEUE_SHORTVIDEO_COMBINE", "shortvideo_combine")


settings = Settings()  # type: ignore
