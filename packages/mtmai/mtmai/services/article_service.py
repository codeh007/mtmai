"""An artifact service implementation using Google Cloud Storage (GCS)."""

import logging
import uuid
from datetime import datetime
from typing import Optional

from google.adk.artifacts.base_artifact_service import BaseArtifactService
from google.genai import types
from sqlalchemy import Text, func
from sqlalchemy.engine import Engine, create_engine
from sqlalchemy.exc import ArgumentError
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column
from sqlalchemy.types import DateTime
from typing_extensions import override

logger = logging.getLogger(__name__)

# 表结构
# CREATE TABLE "artifacts" (
#     "id" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
#     "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
#     "updated_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
#     "type" TEXT,
#     "chat_id" UUID NOT NULL REFERENCES "Chat"(id) ON DELETE CASCADE,
#     "tenant_id" UUID NULL REFERENCES "Tenant"(id) ON DELETE CASCADE,
#     "user_id" UUID NOT NULL REFERENCES "User"(id) ON DELETE CASCADE,
#     "version" INTEGER DEFAULT 1,
#     "session_id" TEXT,
#     "file_name" TEXT,
#     "app_name" TEXT,
#     "title" TEXT,
#     "content" TEXT
# );
# class Base(DeclarativeBase):
#   """Base class for database tables."""


#   pass
class StoreArtifact(DeclarativeBase):
    """Represents an artifact stored in the database."""

    __tablename__ = "artifacts"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=func.now()
    )
    type: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    # chat_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("Chat.id", ondelete="CASCADE"), nullable=False)
    # tenant_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("Tenant.id", ondelete="CASCADE"), nullable=True)
    # user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("User.id", ondelete="CASCADE"), nullable=False)
    version: Mapped[Optional[int]] = mapped_column(default=1)
    session_id: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    file_name: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    app_name: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    title: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    content: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # @property
    # def long_running_tool_ids(self) -> set[str]:
    #     return (
    #         set(json.loads(self.long_running_tool_ids_json))
    #         if self.long_running_tool_ids_json
    #         else set()
    #     )

    # @long_running_tool_ids.setter
    # def long_running_tool_ids(self, value: set[str]):
    #     if value is None:
    #         self.long_running_tool_ids_json = None
    #     else:
    #         self.long_running_tool_ids_json = json.dumps(list(value))


class MtmArtifactService(BaseArtifactService):
    """An artifact service implementation using Google Cloud Storage (GCS)."""

    def __init__(self, db_url: str):
        """Initializes the MtmArtifactService.

        Args:
            bucket_name: The name of the bucket to use.
            **kwargs: Keyword arguments to pass to the Google Cloud Storage client.
        """
        # self.bucket_name = bucket_name
        # self.storage_client = storage.Client(**kwargs)
        # self.bucket = self.storage_client.bucket(self.bucket_name)
        try:
            db_engine = create_engine(db_url)
            self.db_engine: Engine = db_engine
        except Exception as e:
            if isinstance(e, ArgumentError):
                raise ValueError(
                    f"Invalid database URL format or argument '{db_url}'."
                ) from e
            if isinstance(e, ImportError):
                raise ValueError(
                    f"Database related module not found for URL '{db_url}'."
                ) from e
            raise ValueError(
                f"Failed to create database engine for URL '{db_url}'"
            ) from e

    # def _file_has_user_namespace(self, filename: str) -> bool:
    #     """Checks if the filename has a user namespace.

    #     Args:
    #         filename: The filename to check.

    #     Returns:
    #         True if the filename has a user namespace (starts with "user:"),
    #         False otherwise.
    #     """
    #     return filename.startswith("user:")

    # def _get_blob_name(
    #     self,
    #     app_name: str,
    #     user_id: str,
    #     session_id: str,
    #     filename: str,
    #     version: int,
    # ) -> str:
    #     """Constructs the blob name in GCS.

    #     Args:
    #         app_name: The name of the application.
    #         user_id: The ID of the user.
    #         session_id: The ID of the session.
    #         filename: The name of the artifact file.
    #         version: The version of the artifact.

    #     Returns:
    #         The constructed blob name in GCS.
    #     """
    #     if self._file_has_user_namespace(filename):
    #         return f"{app_name}/{user_id}/user/{filename}/{version}"
    #     return f"{app_name}/{user_id}/{session_id}/{filename}/{version}"

    # @override
    # async def save_artifact(
    #     self,
    #     *,
    #     app_name: str,
    #     user_id: str,
    #     session_id: str,
    #     filename: str,
    #     artifact: types.Part,
    # ) -> int:
    #     versions = await self.list_versions(
    #         app_name=app_name,
    #         user_id=user_id,
    #         session_id=session_id,
    #         filename=filename,
    #     )
    #     version = 0 if not versions else max(versions) + 1

    #     blob_name = self._get_blob_name(
    #         app_name, user_id, session_id, filename, version
    #     )
    #     blob = self.bucket.blob(blob_name)

    #     blob.upload_from_string(
    #         data=artifact.inline_data.data,
    #         content_type=artifact.inline_data.mime_type,
    #     )

    #     return version

    @override
    async def load_artifact(
        self,
        *,
        app_name: str,
        user_id: str,
        session_id: str,
        filename: str,
        version: Optional[int] = None,
    ) -> Optional[types.Part]:
        session = Session(self.db_engine)
        artifact = (
            session.query(StoreArtifact)
            .filter(
                StoreArtifact.app_name == app_name,
                StoreArtifact.user_id == user_id,
                StoreArtifact.session_id == session_id,
                StoreArtifact.filename == filename,
                StoreArtifact.version == version,
            )
            .first()
        )
        return artifact

    @override
    async def list_artifact_keys(
        self, *, app_name: str, user_id: str, session_id: str
    ) -> list[str]:
        session = Session(self.db_engine)
        filenames = session.query(StoreArtifact.filename).distinct().all()
        return sorted(list(filenames))

    @override
    async def delete_artifact(
        self, *, app_name: str, user_id: str, session_id: str, filename: str
    ) -> None:
        session = Session(self.db_engine)
        session.query(StoreArtifact).filter(
            StoreArtifact.app_name == app_name,
            StoreArtifact.user_id == user_id,
            StoreArtifact.session_id == session_id,
            StoreArtifact.filename == filename,
        ).delete()
        session.commit()
        return

    @override
    async def list_versions(
        self, *, app_name: str, user_id: str, session_id: str, filename: str
    ) -> list[int]:
        session = Session(self.db_engine)
        versions = session.query(StoreArtifact.version).distinct().all()
        return sorted(list(versions))
