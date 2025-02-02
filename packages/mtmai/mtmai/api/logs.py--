from fastapi import APIRouter, HTTPException

from mtmai.core.logging import get_logger
from mtmai.crud.curd_logs import list_log_items
from mtmai.deps import AsyncSessionDep
from mtmai.models.logitems import LogItemListRequest, LogItemListResponse

router = APIRouter()
logger = get_logger()


@router.post("/logs", response_model=LogItemListResponse)
async def log_list(*, db: AsyncSessionDep, req: LogItemListRequest):
    resource_id = req.resource_id
    if not resource_id:
        raise HTTPException(status_code=400, detail="resource_id is required")
    logitems = await list_log_items(req.app, req.resource_id)
    return logitems
