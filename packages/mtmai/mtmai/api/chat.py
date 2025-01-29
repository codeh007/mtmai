import structlog
from fastapi import APIRouter

router = APIRouter()
LOG = structlog.get_logger()


@router.get("/")
async def chat():
    from mtmai.gomtmclients.rest import ApiClient

    print("ApiClient")
    print(ApiClient)
    return {
        "hello": "chat from python",
    }
