from __future__ import annotations

from datetime import datetime
from typing import Any, ClassVar, Generic, TypeVar

import sqlalchemy as sa
from pydantic import BaseModel, ConfigDict
from sqlalchemy.dialects.postgresql import Insert, insert
from sqlmodel import Field, SQLModel


class MtmBaseSqlModel(SQLModel):
    """Base class for SQL models.
    用途
         1: 作为 基于 SQLModel 的自定义基类
         2: 添加 upsert的支持, 参考: https://github.com/dan1elt0m/sadel/blob/main/sadel/base.py
    """

    model_config = ConfigDict(validate_assignment=True)  # pyright: ignore
    created_at: datetime | None = Field(
        default=None,
        sa_type=sa.DateTime(timezone=True),  # type: ignore
        sa_column_kwargs={"server_default": sa.func.now()},
        description=(
            "The date and time the record was created. "
            "Field is optional and not needed when instantiating a new record. "
            "It will be automatically set when the record is created in the database."
        ),
    )

    updated_at: datetime | None = Field(
        default=None,
        sa_type=sa.DateTime(timezone=True),  # pyright: ignore
        sa_column_kwargs={"onupdate": sa.func.now(), "server_default": sa.func.now()},
        description=(
            "The date and time the record was updated. "
            "Field is optional and not needed when instantiating a new record. "
            "It will be automatically set when the record is created in the database."
        ),
    )

    # Specifies the set of index elements which represent the ON CONFLICT target
    _upsert_index_elements: ClassVar[set[str]] = set()

    # Specifies the set of fields to exclude from updating in the resulting
    # UPSERT statement
    _upsert_exclude_fields: ClassVar[set[str]] = set()

    # Common fields which we should exclude when updating.
    _default_upsert_exclude_fields: ClassVar[set[str]] = {"created_at"}

    @classmethod
    async def upsert(cls, item: MtmBaseSqlModel, session: sa.orm.Session):
        """upserts a single item"""
        stmt = cls._get_upsert_statement(item)
        await session.exec(stmt)
        await session.commit()

    @classmethod
    async def batch_upsert(cls, items: list[MtmBaseSqlModel], session: sa.orm.Session):
        """Batch upserts a list of items."""
        for item in items:
            stmt = cls._get_upsert_statement(item)
            await session.exec(stmt)
        await session.commit()

    @classmethod
    def _get_upsert_statement(cls, item: MtmBaseSqlModel) -> Insert:
        """Returns an UPSERT statement for a single item."""
        if not cls._upsert_index_elements:
            raise ValueError("No upsert index elements specified for the model.")

        to_insert = item.model_dump()
        to_insert["created_at"] = (
            sa.func.now()
        )  # set manually, because on_conflict_do_update doesn't trigger default oninsert
        to_update = cls._get_record_to_update(to_insert)
        stmt = insert(cls).values(to_insert)
        return stmt.on_conflict_do_update(
            index_elements=cls._upsert_index_elements,
            set_=to_update,
        )

    @classmethod
    def _get_record_to_update(cls, record: dict[str, Any]) -> dict[str, Any]:
        """Returns a record to be upserted taking into account the excluded fields."""
        exclude_fields = cls._upsert_exclude_fields.copy()
        exclude_fields.update(cls._default_upsert_exclude_fields)

        to_update = record.copy()

        for field in exclude_fields:
            _ = to_update.pop(field, None)  # pyright: ignore

        to_update["updated_at"] = (
            sa.func.now()
        )  # set manually. on_conflict_do_update doesn't trigger onupdate

        return to_update  # type: ignore


class CommonResultRequest(BaseModel):
    q: str | None = Field(default=None, max_length=255)
    skip: int = Field(default=0)
    limit: int = Field(default=10)


class CommonResultResponse(BaseModel):
    error: str = Field(default="")
    data: dict = Field(default={})
    message: str = Field(default="")


T = TypeVar("T")


class ListResponse(BaseModel, Generic[T]):
    count: int
    items: list[T]
