import logging
import time

import httpx
import uiautomator2 as u2
from playwright.async_api import async_playwright

logger = logging.getLogger(__name__)


class InstBot:
  android_package_name = "com.instagram.android"
  android_apk_url = "https://apk2.yuepa8.com/apk/instgram_v2.apk"

  def __init__(self, device_serial: str):
    self.device = u2.connect(device_serial)
    self.cdp_ws_endpoint = None
    # self.dev_adb_ip = None
    # device_serial 冒号分隔,第一部分,就是主机名

    # 设备主机名
    self.dev_host = device_serial.split(":")[0]
    # 获取设备信息
    self.device_info = self.get_device_info()

  def get_device_info(self):
    """获取设备信息"""
    try:
      info = {}
      # 获取设备基本信息
      try:
        # 正确处理ShellResponse对象
        brand = self.device.shell("getprop ro.product.brand")
        info["brand"] = str(brand).strip() if brand else "unknown"

        model = self.device.shell("getprop ro.product.model")
        info["model"] = str(model).strip() if model else "unknown"

        android_version = self.device.shell("getprop ro.build.version.release")
        info["android_version"] = str(android_version).strip() if android_version else "unknown"

        sdk_version = self.device.shell("getprop ro.build.version.sdk")
        info["sdk_version"] = str(sdk_version).strip() if sdk_version else "unknown"
      except Exception as e:
        logger.warning(f"获取设备基本信息失败: {e}")

      # 获取设备分辨率
      try:
        window_size = self.device.window_size()
        info["resolution"] = f"{window_size[0]}x{window_size[1]}"
      except Exception as e:
        logger.warning(f"获取设备分辨率失败: {e}")

      # 获取设备IP地址
      try:
        ip_result = self.device.shell("ifconfig | grep 'inet '")
        ip_result_str = str(ip_result) if ip_result else ""

        if ip_result_str:
          import re

          ip_matches = re.findall(r"inet\s+(\d+\.\d+\.\d+\.\d+)", ip_result_str)
          if ip_matches:
            for ip in ip_matches:
              if not ip.startswith("127."):  # 排除localhost
                info["ip_address"] = ip
                break
      except Exception as e:
        logger.warning(f"获取IP地址时出错: {e}")

      # 获取设备序列号
      info["serial"] = self.device.serial

      logger.info(f"设备信息: {info}")
      return info
    except Exception as e:
      logger.error(f"获取设备信息失败: {e}")
      return {}

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
    await self.login()
    # else:
    #   logger.info("未知的 instgram 状态")

  async def login(self):
    self.open_android_chrome_with_cdp()
    async with async_playwright() as p:
      browser = await p.chromium.connect_over_cdp(f"http://{self.dev_host}:9222")
      context = browser.contexts[0]
      page = context.pages[0]
      await page.goto("https://www.bing.com")
      await page.screenshot(path="example.png")
      await page.close()
      await browser.close()

  def open_android_chrome_with_cdp(self):
    """设置并启动支持CDP的Chrome浏览器"""

    chrome_package = "com.android.chrome"

    # app_list = self.device.app_list()
    # if chrome_package not in app_list:
    #   logger.error("Chrome未安装在设备上，请先安装Chrome")
    #   return False

    # 关闭所有Chrome进程以确保干净启动
    # self.device.app_stop(chrome_package)
    # time.sleep(1)

    try:
      self.device.shell(
        "am start -a android.intent.action.VIEW -d 'about:blank' --ez 'enable-remote-debugging' true com.android.chrome"
      )
    except Exception:
      self.device.shell(
        'am start -n com.android.chrome/com.google.android.apps.chrome.Main --ez "enable-remote-debugging" true'
      )

    # 等待Chrome启动
    time.sleep(3)

    http_url = f"http://{self.dev_host}:9222"
    logger.info(f"http_url: {http_url}")
    response = httpx.get(http_url)
    logger.info(f"response: {response.text}")

    # # 设置端口转发
    # # 使用本机执行adb forward命令
    # device_serial = self.device.serial

    # # 先清除可能存在的端口转发
    # subprocess.run(
    #   f"adb -s {device_serial} forward --remove tcp:9222",
    #   shell=True,
    #   stdout=subprocess.PIPE,
    #   stderr=subprocess.PIPE,
    # )
    # time.sleep(1)

    # # 执行端口转发
    # cmd = f"adb -s {device_serial} forward tcp:9222 localabstract:chrome_devtools_remote"
    # logger.info(f"执行命令: {cmd}")
    # result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

    # if result.returncode != 0:
    #   logger.error(f"端口转发失败: {result.stderr}")
    #   return False

    # # 等待CDP服务启动
    # time.sleep(1)

    # # 确保Chrome已经完全启动并且CDP服务可用
    # self.device.shell("input keyevent KEYCODE_BACK")  # 返回键，确保Chrome处于活动状态
    # time.sleep(1)

    # # 验证本地端口转发是否成功
    # local_check_cmd = "curl -s http://localhost:9222/json/version"
    # logger.info(f"验证本地端口转发: {local_check_cmd}")
    # local_result = subprocess.run(local_check_cmd, shell=True, capture_output=True, text=True)

    # if local_result.returncode == 0 and local_result.stdout:
    #   logger.info(f"本地CDP服务验证成功: {local_result.stdout[:100]}...")
    # else:
    #   logger.warning(f"本地CDP服务验证失败: {local_result.stderr}")
    #   # 尝试再次启动Chrome
    #   logger.info("尝试再次启动Chrome...")
    #   self.device.shell(
    #     'am start -n com.android.chrome/com.google.android.apps.chrome.Main --ez "enable-remote-debugging" true'
    #   )
    #   time.sleep(3)
    return True
