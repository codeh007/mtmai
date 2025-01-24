from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import structlog

from mtmai.crud import curd_chat
from mtmai.deps import OptionalUserDep

router = APIRouter()
LOG = structlog.get_logger()



@router.get("/thread/{thread_id}/element/{element_id}")
async def get_thread_element(
    thread_id: str,
    element_id: str,
    user: OptionalUserDep,
):
    """Get a specific thread element."""
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    ok = await curd_chat.is_thread_author(user.id, thread_id)
    if not ok:
        raise HTTPException(status_code=401, detail="Unauthorized")

    item = await curd_chat.get_chat_element(thread_id, element_id)
    if not item:
        raise HTTPException(status_code=404, detail="Element not found")
    return JSONResponse(content=item)
