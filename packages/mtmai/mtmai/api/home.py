from fastapi import APIRouter
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_oauth2_redirect_html
from loguru import logger
from opentelemetry import trace

from mtmai.core.config import settings

tracer = trace.get_tracer_provider().get_tracer(__name__)
router = APIRouter()


@router.get("/health", include_in_schema=False)
async def health_check():
    with tracer.start_as_current_span("health-span"):
        logger.info("get /health")
        current_span = trace.get_current_span()
        current_span.add_event("This is a span event")
        logger.warning("This is a log message")
        return {"health": True}


@router.get("/swagger-ui-oauth2-redirect", include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()


@router.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=router.app().openapi_url,
        title=router.app().title + " - ReDoc",
        redoc_js_url="https://unpkg.com/redoc@next/bundles/redoc.standalone.js",
    )


@router.get("/info", include_in_schema=False)
async def app_info():
    return {
        "app_name": settings.app_name,
        "admin_email": settings.admin_email,
        "items_per_user": settings.items_per_user,
    }
