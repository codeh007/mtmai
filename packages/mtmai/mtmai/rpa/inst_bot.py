import logging

import uiautomator2 as u2

logger = logging.getLogger(__name__)


class InstBot:
  android_package_name = "com.instagram.android"
  android_apk_url = "https://apk2.yuepa8.com/apk/instgram_v2.apk"

  def __init__(self, device_serial: str):
    self.device = u2.connect(device_serial)

  async def install_apk(self):
    app_list = self.device.app_list()
    # 如果没安装就安装
    if self.android_package_name not in app_list:
      self.device.app_install(self.android_apk_url)

  async def start(self):
    # 如果没启动就启动
    await self.install_apk()
    app_running_list = self.device.app_list_running()
    logger.info(f"app_running_list: {app_running_list}")
    if self.android_package_name not in app_running_list:
      self.device.app_start(self.android_package_name)
    else:
      logger.info(f"app {self.android_package_name} is already running")

    # 获取应用的登录UI 状态, 如果是登录框,就进行登录
    login_ui_status = self.device.xpath('//*[@content-desc="登入"]').exists
    # if login_ui_status:
    self.login()
    # else:
    #   logger.info("未知的 instgram 状态")

  def login(self):
    logger.info("TODO: login instgram")
    self.open_android_chrome_with_cdp()

  def open_android_chrome_with_cdp(self):
    self.device.shell("am start -a android.intent.action.VIEW -d 'https://www.google.com'")
