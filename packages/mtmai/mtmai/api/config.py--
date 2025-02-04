from fastapi import APIRouter
from pydantic import BaseModel
import structlog

from mtmai.core import coreutils
from mtmai.core.config import settings

router = APIRouter()
LOG = structlog.get_logger()



class AppConfig(BaseModel):
    """客户端应用的核心配置项"""

    theme: str = "light"
    articleUrlBase: str = "https://www.mtmai.com"
    apiPrefix: str = settings.API_V1_STR


@router.get("/config/app", response_model=AppConfig)
async def get_app_config():
    """获取客户端应用的核心配置项"""
    backend_url_base = coreutils.backend_url_base()
    return AppConfig(articleUrlBase=backend_url_base, apiPrefix=settings.API_V1_STR)
