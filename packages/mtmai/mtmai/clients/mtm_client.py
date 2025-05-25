import json
import logging
import os
from functools import cache
from typing import Any

from mtmai.clients.rest.api.ag_state_api import AgStateApi
from mtmai.clients.rest.api.artifact_api import ArtifactApi
from mtmai.clients.rest.api.browser_api import BrowserApi
from mtmai.clients.rest.api.chat_api import ChatApi
from mtmai.clients.rest.api.flow_state_api import FlowStateApi
from mtmai.clients.rest.api.platform_account_api import PlatformAccountApi
from mtmai.clients.rest.api.resource_api import ResourceApi
from mtmai.clients.rest.api.user_api import UserApi
from mtmai.clients.rest.api_client import ApiClient
from mtmai.clients.rest.configuration import Configuration
from mtmai.clients.rest.models.user_login_request import UserLoginRequest
from mtmai.core.config import settings

logger = logging.getLogger(__name__)


def get_client_config_path():
  config_path = os.path.expanduser("~/.mtm/config.json")
  os.makedirs(os.path.dirname(config_path), exist_ok=True)
  return config_path


@cache
def get_tenant_id():
  with open(get_client_config_path(), "r") as f:
    config = json.load(f)
    return config.get("tenant_id")


class MtmClient:
  def __init__(self, server_url: str | None = None, access_token: str | None = None):
    self.server_url = server_url or settings.MTM_SERVER_URL
    self.access_token = access_token
    logger.info(f"get_client_config_path(): {get_client_config_path()}")
    if not self.access_token:
      if not os.path.exists(get_client_config_path()):
        raise ValueError(f"未登录: {get_client_config_path()}")
      with open(get_client_config_path(), "r") as f:
        config = json.load(f)
        self.access_token = config.get("access_token")
        self.tenant_id: str = config.get("tenant_id")

  @classmethod
  async def login(cls):
    """登录"""
    username = input("请输入用户名: ")
    password = input("请输入密码: ")
    async with ApiClient(
      configuration=Configuration(
        host=settings.MTM_SERVER_URL,
      )
    ) as api_client:
      user_api = UserApi(api_client)
      login_response = await user_api.user_update_login(UserLoginRequest(email=username, password=password))
      if not login_response.user_token:
        raise ValueError(f"登录失败: {login_response.message}")
      access_token = login_response.user_token

      # 获取 tenant 信息
      tenant_memberships = await user_api.tenant_memberships_list()
      tenant_id = tenant_memberships.rows[0].metadata.id

      client_config_path = get_client_config_path()
      logger.info(f"登录成功, tenant_id: {tenant_id}")
      with open(client_config_path, "w") as f:
        json.dump({"email": username, "access_token": access_token, "tenant_id": tenant_id}, f)

  @classmethod
  def tenant_id(cls):
    if not hasattr(cls, "_tenant_id"):
      with open(get_client_config_path(), "r") as f:
        config = json.load(f)
        cls._tenant_id = config.get("tenant_id")
    return cls._tenant_id

  @property
  def api_client(self):
    if hasattr(self, "_api_client"):
      return self._api_client
    self._api_client = ApiClient(configuration=Configuration(host=self.server_url, access_token=self.access_token))
    return self._api_client

  @property
  def ag_state_api(self):
    if hasattr(self, "_ag_state_api"):
      return self._ag_state_api
    self._ag_state_api = AgStateApi(self.api_client)
    return self._ag_state_api

  @property
  def user_api(self):
    if hasattr(self, "_user_api"):
      return self._user_api
    self._user_api = UserApi(self.api_client)
    return self._user_api

  @property
  def artifact_api(self):
    if hasattr(self, "_artifact_api"):
      return self._artifact_api
    self._artifact_api = ArtifactApi(self.api_client)
    return self._artifact_api

  @property
  def platform_account_api(self):
    if hasattr(self, "_platform_account_api"):
      return self._platform_account_api
    self._platform_account_api = PlatformAccountApi(self.api_client)
    return self._platform_account_api

  @property
  def resource_api(self):
    if hasattr(self, "_resource_api"):
      return self._resource_api
    self._resource_api = ResourceApi(self.api_client)
    return self._resource_api

  @property
  def flow_state_api(self):
    if hasattr(self, "_flow_state_api"):
      return self._flow_state_api
    self._flow_state_api = FlowStateApi(self.api_client)
    return self._flow_state_api

  @property
  def chat_api(self):
    if hasattr(self, "_chat_api"):
      return self._chat_api
    self._chat_api = ChatApi(self.api_client)
    return self._chat_api

  @property
  def browser_api(self):
    if hasattr(self, "_browser_api"):
      return self._browser_api
    self._browser_api = BrowserApi(self.api_client)
    return self._browser_api

  async def emit(self, event: Any):
    await self.event.emit(event)
