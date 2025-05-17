import uuid
from datetime import datetime
from uuid import UUID

from sqlmodel import Column, DateTime, Field, SQLModel, func


class MtTask(SQLModel, table=False):
  task: str


class MtTaskStep(SQLModel, table=False):
  id: UUID = Field(default_factory=uuid.uuid4)
  task_id: UUID
  #   created_at: datetime
  #   updated_at: datetime
  created_at: datetime = Field(
    default_factory=datetime.now,
    sa_column=Column(DateTime(timezone=True), server_default=func.now()),
  )  # pylint: disable=not-callable
  updated_at: datetime = Field(
    default_factory=datetime.now,
    sa_column=Column(DateTime(timezone=True), onupdate=func.now()),
  )  # pylint: disable=not-callable
  data: dict
