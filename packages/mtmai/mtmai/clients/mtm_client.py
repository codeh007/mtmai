import json
import os
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
from pydantic import BaseModel

# def parser_ctx_from_metas(meta: dict[str, str]):
#   if META_RUN_BY_TENANT in meta:
#     set_tenant_id(meta[META_RUN_BY_TENANT])
#   if META_SESSION_ID in meta:
#     set_chat_session_id_ctx(meta[META_SESSION_ID])
#   if META_RUN_BY_USER_ID in meta:
#     set_run_by_user_id_ctx(meta[META_RUN_BY_USER_ID])


# def parse_ctx_from_action(action: Action):
#   set_run_id(action.workflow_run_id)
#   set_step_run_id(action.step_run_id)
#   parser_ctx_from_metas(action.additional_metadata)


class ClientConfig(BaseModel):
  server_url: str
  access_token: str | None = None


class MtmClient:
  def __init__(self, server_url: str | None = None, access_token: str | None = None):
    # set_server_url_ctx(settings.MTM_SERVER_URL)
    self.server_url = server_url
    if not self.server_url:
      self.server_url = settings.MTM_SERVER_URL
    self.access_token = access_token
    if not self.access_token:
      if not os.path.exists(settings.MTM_CREDENTIALS):
        raise ValueError(f"config file not found: {settings.MTM_CREDENTIALS}")
      with open(settings.MTM_CREDENTIALS, "r") as f:
        config = json.load(f)
        self.access_token = config.get("access_token")

    # self.tenant_id = get_tenant_id()
    # assert self.tenant_id is not None
    # self.run_id = get_run_id()
    # self.step_run_id = get_step_run_id()
    # self.session_id = get_chat_session_id_ctx()
    # self.server_url = get_server_url()
    # if self.server_url is None:
    #   raise ValueError("server_url context is not set")
    # self.access_token = get_access_token()
    # if self.access_token is None:
    #   raise ValueError("access_token context is not set")

    # server_url = settings.MTM_SERVER_URL

    # access_token = None
    # if not os.path.exists(settings.MTM_CREDENTIALS):
    #   raise ValueError(f"config file not found: {settings.MTM_CREDENTIALS}")
    # with open(settings.MTM_CREDENTIALS, "r") as f:
    #   config = json.load(f)
    #   access_token = config.get("access_token")
    # self.client_config = ClientConfig(server_url=server_url, access_token=access_token)

    # host = urlparse(server_url).netloc
    # self.client_config = Configuration(
    #   host=host,
    #   # access_token=self.access_token,
    # )

  async def init(self):
    pass

  @classmethod
  async def login(cls):
    """登录"""

    client_config_path = os.path.expanduser(settings.MTM_CREDENTIALS)
    if not os.path.exists(client_config_path):
      username = input("请输入用户名: ")
      password = input("请输入密码: ")
      user_api = UserApi(
        ApiClient(
          configuration=Configuration(
            host=settings.MTM_SERVER_URL,
          )
        )
      )
      login_response = await user_api.user_update_login(UserLoginRequest(email=username, password=password))
      if not login_response.user_token:
        raise ValueError(f"登录失败: {login_response.message}")
      access_token = login_response.user_token
      with open(client_config_path, "w") as f:
        json.dump({"email": username, "access_token": access_token}, f)

  @property
  def api_client(self):
    if self._api_client is None:
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

  # async def get_mcp_endpoint(self):
  #     server_params = SseServerParams(
  #         url="http://localhost:8383/mcp/sse",
  #         headers={"Authorization": "Bearer token"},
  #     )
  #     return server_params
