"""
为前端，以 openapi 的方式生成类型

"""

from email.policy import default
from typing import Literal
from pydantic import BaseModel


class DashNavItem(BaseModel):
    """
    菜单导航
    目前 以列表的方式表示，
    以后升级为树
    """

    title: str | None = None
    label: str | None = None
    icon: str | None = None
    url: str | None = None
    variant: Literal["ghost", "default"] | None = "default"
    tooltip: str | None = None


class DashConfig(BaseModel):
    """管理面板的后台配置"""

    logo: str | None = None
    pathPrefix: str | None = "/"
    navMenus: list[DashNavItem] | None = []
    loginUrl: str = "/auth/login"
    theme: str | None = "light"
    layout: str | None = "default"


class CmdkItem(BaseModel):
    """
    命令行菜单
    """

    label: str | None = None
    icon: str | None = None
    url: str | None = (
        None  # 用url的方式表示命令名称及参数, 例如： mtmai://local.mtmai.cmd?file_path=/data/data.json
    )
