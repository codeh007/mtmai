"""博客系统的 curd 操作"""

from datetime import datetime

from fastapi import HTTPException
from pydantic import BaseModel
from sqlmodel import select

from mtmai.db.db import get_async_session
from mtmai.models.logitems import LogItem, LogItemListResponse


class LogItemCreateReq(BaseModel):
    app: str
    text: str
    level: int = 3
    resource_id: str | None = None


async def create_log_item(
    log_item_create: LogItemCreateReq,
) -> LogItem:
    input_data = LogItemCreateReq.model_validate(log_item_create)

    if not input_data.text:
        raise HTTPException(status_code=400, detail="text is required")
    if not input_data.app:
        input_data = "sys"

    async with get_async_session() as session:
        new_log_item = LogItem(**input_data.model_dump(), title="text")
        session.add(new_log_item)
        await session.commit()
        await session.refresh(new_log_item)
    return new_log_item


async def create_context_logger():
    pass


async def list_log_items(app: str, resource_id: str | None = None):
    async with get_async_session() as session:
        query = select(LogItem).where(
            LogItem.app == app,
            LogItem.is_deleted == False,  # noqa: E712
            LogItem.expire_at > datetime.now(),
            LogItem.resource_id == resource_id,
        )
        if resource_id:
            query = query.where(LogItem.resource_id == resource_id)
        result = await session.exec(query)
        items = result.all()

        return LogItemListResponse(items=items, total=len(items))
