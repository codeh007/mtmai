import logging
import subprocess
import time

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
    """设置并启动支持CDP的Chrome浏览器"""
    logger.info("Setting up Chrome for remote debugging...")

    # Chrome包名
    chrome_package = "com.android.chrome"

    # 检查Chrome是否已安装
    app_list = self.device.app_list()
    if chrome_package not in app_list:
      logger.error("Chrome未安装在设备上，请先安装Chrome")
      return False

    # 关闭所有Chrome进程以确保干净启动
    self.device.app_stop(chrome_package)
    time.sleep(1)

    # 以远程调试模式启动Chrome
    logger.info("启动Chrome并开启远程调试...")
    # 使用正确的方式启动Chrome并开启远程调试
    try:
      # 方法1：直接使用命令行参数启动
      self.device.shell(
        "am start -a android.intent.action.VIEW -d 'about:blank' --ez 'enable-remote-debugging' true com.android.chrome"
      )
      time.sleep(3)
    except Exception as e:
      logger.warning(f"使用方法1启动Chrome失败: {e}")
      try:
        # 方法2：使用另一种命令格式
        self.device.shell(
          'am start -n com.android.chrome/com.google.android.apps.chrome.Main --ez "enable-remote-debugging" true'
        )
        time.sleep(3)
      except Exception as e2:
        logger.error(f"启动Chrome失败: {e2}")
        return False

    # 使用固定的内网IP
    ip_address = "100.95.167.78"
    logger.info(f"使用固定IP地址: {ip_address}")

    # 设置端口转发
    try:
      # 使用本机执行adb forward命令
      device_serial = self.device.serial

      # 先清除可能存在的端口转发
      subprocess.run(
        f"adb -s {device_serial} forward --remove tcp:9222", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
      )
      time.sleep(1)

      # 执行端口转发
      cmd = f"adb -s {device_serial} forward tcp:9222 localabstract:chrome_devtools_remote"
      logger.info(f"执行命令: {cmd}")
      result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

      if result.returncode != 0:
        logger.error(f"端口转发失败: {result.stderr}")
        return False

      # 等待CDP服务启动
      time.sleep(3)

      # 确保Chrome已经完全启动并且CDP服务可用
      self.device.shell("input keyevent KEYCODE_BACK")  # 返回键，确保Chrome处于活动状态
      time.sleep(1)

      # 尝试访问一个简单的网页，确保Chrome已正确启动
      self.device.shell("am start -a android.intent.action.VIEW -d 'https://www.baidu.com' com.android.chrome")
      time.sleep(3)

      # 验证本地端口转发是否成功
      local_check_cmd = "curl -s http://localhost:9222/json/version"
      logger.info(f"验证本地端口转发: {local_check_cmd}")
      local_result = subprocess.run(local_check_cmd, shell=True, capture_output=True, text=True)

      if local_result.returncode == 0 and local_result.stdout:
        logger.info(f"本地CDP服务验证成功: {local_result.stdout[:100]}...")
      else:
        logger.warning(f"本地CDP服务验证失败: {local_result.stderr}")

      # 提供两个可能的调试地址
      logger.info("Chrome远程调试已设置。")
      logger.info("本地调试地址: http://localhost:9222")
      logger.info(f"远程调试地址: http://{ip_address}:9222")

      return True
    except Exception as e:
      logger.error(f"设置Chrome远程调试失败: {e}")
      return False
