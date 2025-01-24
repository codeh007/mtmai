import structlog
from fastapi import APIRouter

router = APIRouter()
LOG = structlog.get_logger()


@router.get("/hello")
async def ag_hello(messageId: str):
    {
        "hello": "ag",
    }
