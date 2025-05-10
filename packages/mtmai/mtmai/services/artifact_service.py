"""An artifact service implementation using Google Cloud Storage (GCS)."""

import logging
import uuid
from datetime import datetime
from typing import Optional

from google.adk.artifacts.base_artifact_service import BaseArtifactService
from google.genai import types
from mtmai.db.db import get_async_session
from mtmai.mtlibs.mtfs import get_s3fs
from sqlalchemy import delete, func

# from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column
from sqlmodel import Field, SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession
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
#     """Base class for database tables."""

#     pass


class StoreArtifact(SQLModel, table=True):
    """Represents an artifact stored in the database."""

    __tablename__ = "artifacts"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(
        default_factory=datetime.now,
        nullable=False,
    )
    updated_at: datetime = Field(
        default_factory=datetime.now,
        nullable=False,
    )
    type: str | None = Field(default=None)
    version: int | None = Field(default=1)
    session_id: str | None = Field(default=None)
    file_name: str | None = Field(default=None)
    app_name: str | None = Field(default=None)
    title: str | None = Field(default=None)
    content: str | None = Field(default=None)


class MtmArtifactService(BaseArtifactService):
    """An artifact service implementation 使用 postgresql 存储构件, 列表数据存入表, 文件存入第三方aws s3"""

    def __init__(self, db_url: str):
        """Initializes the MtmArtifactService.

        Args:
            bucket_name: The name of the bucket to use.
            **kwargs: Keyword arguments to pass to the Google Cloud Storage client.
        """
        self.bucket_name = ""
        # self.storage_client = storage.Client(**kwargs)
        # self.bucket = self.storage_client.bucket(self.bucket_name)
        # try:
        #     db_engine = create_async_engine(db_url)
        #     self.db_engine: Engine = db_engine
        # except Exception as e:
        #     if isinstance(e, ArgumentError):
        #         raise ValueError(
        #             f"Invalid database URL format or argument '{db_url}'."
        #         ) from e
        #     if isinstance(e, ImportError):
        #         raise ValueError(
        #             f"Database related module not found for URL '{db_url}'."
        #         ) from e
        #     raise ValueError(
        #         f"Failed to create database engine for URL '{db_url}'"
        #     ) from e

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

    @override
    async def save_artifact(
        self,
        *,
        app_name: str,
        user_id: str,
        session_id: str,
        filename: str,
        artifact: types.Part,
    ) -> int:
        s3fs = get_s3fs()

        # 例子: get_s3fs().upload_file(audio_file, f"short_videos/audio-{ctx.session.id}.mp3")
        # temp_file = BytesIO()
        # temp_file.write(artifact.inline_data.data)
        # temp_file.seek(0)
        await s3fs.put_object(
            artifact.inline_data.data,
            f"{app_name}/{user_id}/{session_id}/{filename}",
        )

        async with get_async_session() as session:
            # Get current max version for this artifact
            result = await session.exec(
                select(func.max(StoreArtifact.version)).where(
                    StoreArtifact.app_name == app_name,
                    StoreArtifact.user_id == user_id,
                    StoreArtifact.session_id == session_id,
                    StoreArtifact.filename == filename,
                )
            )
            current_version = result.scalar() or 0
            new_version = current_version + 1

            # Create new artifact with incremented version
            new_artifact = StoreArtifact(
                app_name=app_name,
                user_id=user_id,
                session_id=session_id,
                filename=filename,
                version=new_version,
                artifact=artifact,
            )
            session.add(new_artifact)
            await session.commit()

            return new_version

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
        async with AsyncSession(self.db_engine) as session:
            statement = select(StoreArtifact).where(
                StoreArtifact.app_name == app_name,
                StoreArtifact.user_id == user_id,
                StoreArtifact.session_id == session_id,
                StoreArtifact.filename == filename,
                StoreArtifact.version == version,
            )
            result = await session.exec(statement)
            artifact = result.first()
            return artifact

    @override
    async def list_artifact_keys(
        self, *, app_name: str, user_id: str, session_id: str
    ) -> list[str]:
        async with AsyncSession(self.db_engine) as session:
            statement = select(StoreArtifact.filename).distinct()
            result = await session.exec(statement)
            filenames = result.all()
            return sorted(list(filenames))

    @override
    async def delete_artifact(
        self, *, app_name: str, user_id: str, session_id: str, filename: str
    ) -> None:
        async with AsyncSession(self.db_engine) as session:
            await session.exec(
                delete(StoreArtifact).where(
                    StoreArtifact.app_name == app_name,
                    StoreArtifact.user_id == user_id,
                    StoreArtifact.session_id == session_id,
                    StoreArtifact.filename == filename,
                )
            )
            await session.commit()
        return

    @override
    async def list_versions(
        self, *, app_name: str, user_id: str, session_id: str, filename: str
    ) -> list[int]:
        async with AsyncSession(self.db_engine) as session:
            statement = select(StoreArtifact.version).distinct()
            result = await session.exec(statement)
            versions = result.all()
            return sorted(list(versions))
