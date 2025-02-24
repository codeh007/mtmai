import json

from fastapi.encoders import jsonable_encoder
from sqlmodel import delete

from mtmai.db.db import get_async_session
from mtmai.models.kv import Mtkv


async def mtkv_get(key: str):
    async with get_async_session() as session:
        item = await session.query(Mtkv).filter(Mtkv.key == key)
        str_v = item.first()
        if str_v:
            return json.loads(str_v.value)
        return None


async def mtkv_set(key: str, value: any):
    value = jsonable_encoder(value)
    async with get_async_session() as session:
        session.add(Mtkv(key=key, value=json.dumps(value)))
        await session.commit()


async def mtkv_delete(key: str):
    async with get_async_session() as session:
        stmt = delete(Mtkv).where(Mtkv.key == key)
        await session.exec(stmt)
        await session.commit()
