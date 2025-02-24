from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from mtmai.models.models import SysItem


async def get_sys_items(session: AsyncSession, type: str):
    result = await session.exec(select(SysItem).where(SysItem.type == type))
    return result.all()
