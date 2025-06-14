import logging
from typing import Optional

from google.adk.artifacts.base_artifact_service import BaseArtifactService
from google.genai import types
from sqlalchemy import delete
from sqlmodel import select
from typing_extensions import override

from mtmai.clients.mtm_client import MtmClient
from mtmai.clients.rest.models.artifact import Artifact
from mtmai.clients.rest.models.save_artifact_request import SaveArtifactRequest
from mtmai.db.db import get_async_session
from mtmai.models.artifact import DBArtifact
from mtmai.mtlibs.mtfs import get_s3fs

logger = logging.getLogger(__name__)


class MtmArtifactService(BaseArtifactService):
  """An artifact service implementation 使用 postgresql 存储构件, 列表数据存入表, 文件存入第三方aws s3"""

  def __init__(self):
    self.bucket_name = ""
    # self.tenant_id = tenant_id
    self.mtm_client = MtmClient()

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
    await s3fs.put_object(
      artifact.inline_data.data,
      f"{app_name}/{user_id}/{session_id}/{filename}",
    )

    result: Artifact = await self.mtm_client.artifact_api.artifact_save(
      tenant=self.tenant_id,
      save_artifact_request=SaveArtifactRequest(
        app_name=app_name,
        artifact=filename,
        user_id=user_id,
        session_id=session_id,
        filename=filename,
        content=artifact.inline_data.data,
        mime_type=artifact.inline_data.mime_type.encode()("utf-8"),
      ),
    )
    logger.info(f"save_artifact result: {result}")
    return result.version

    # async with get_async_session() as session:
    #   result = await session.exec(
    #     text("""
    #             SELECT * FROM public.insert_artifact(:p_user_id, :p_session_id, :p_file_name, :p_app_name, :p_type, :p_content);
    #         """),
    #     params={
    #       "p_user_id": user_id,
    #       "p_session_id": session_id,
    #       "p_app_name": app_name,
    #       "p_file_name": filename,
    #       "p_type": artifact.inline_data.mime_type,
    #       "p_content": artifact.inline_data.data,
    #     },
    #   )
    #   new_artifact = result.fetchone()
    #   return new_artifact.version

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
    async with get_async_session() as session:
      statement = select(DBArtifact).where(
        DBArtifact.app_name == app_name,
        # StoreArtifact.user_id == user_id,  # TODO: 需要根据用户id查询
        DBArtifact.session_id == session_id,
        DBArtifact.filename == filename,
        DBArtifact.version == version,
      )
      result = await session.exec(statement)
      artifact = result.first()
      return artifact

  @override
  async def list_artifact_keys(self, *, app_name: str, user_id: str, session_id: str) -> list[str]:
    async with get_async_session() as session:
      statement = select(DBArtifact.filename).distinct()
      result = await session.exec(statement)
      filenames = result.all()
      return sorted(list(filenames))

  @override
  async def delete_artifact(self, *, app_name: str, user_id: str, session_id: str, filename: str) -> None:
    async with get_async_session() as session:
      await session.exec(
        delete(DBArtifact).where(
          DBArtifact.app_name == app_name,
          # StoreArtifact.user_id == user_id, # TODO: 需要根据用户id删除
          DBArtifact.session_id == session_id,
          DBArtifact.filename == filename,
        )
      )
      await session.commit()
    return

  @override
  async def list_versions(self, *, app_name: str, user_id: str, session_id: str, filename: str) -> list[int]:
    async with get_async_session() as session:
      statement = select(DBArtifact.version).distinct()
      result = await session.exec(statement)
      versions = result.all()
      return sorted(list(versions))
