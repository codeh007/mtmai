import logging

import uiautomator2 as u2
from mtmai.rpa.android_apps_config import get_android_app_info
from mtmai.rpa.rpa_consts import ANDROID_LOCAL_SHARED_DIR

logger = logging.getLogger(__name__)


def launch_app(device: u2.Device, package_name: str):
  """启动应用
     1: 如果应用未安装,则安装
     2: 如果应用未运行,则启动

  Args:
      device (u2.Device): 设备
      package_name (str): 应用包名

  Raises:
      Exception: _description_
  """

  app_info = get_android_app_info(package_name)

  app_list = device.app_list()
  if package_name not in app_list:
    logger.info(f"App {app_info['app_name']} is not installed, installing...")
    device.app_install(f"{ANDROID_LOCAL_SHARED_DIR}/apk/{app_info['apk_url']}")
  device.app_start(app_info["package_name"])
