import asyncio
import logging
import subprocess
import time

import requests
import uiautomator2 as u2

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
    # 首先设置CDP
    if self.open_android_chrome_with_cdp():
      logger.info("CDP设置成功，准备使用Playwright进行自动化")
      # 创建一个事件循环来运行异步函数
      loop = asyncio.get_event_loop()
      try:
        # 运行Playwright示例
        result = loop.run_until_complete(self.example_playwright_automation())
        if result:
          logger.info("Playwright自动化示例执行成功")
        else:
          logger.warning("Playwright自动化示例执行失败")
      except Exception as e:
        logger.error(f"运行Playwright示例时出错: {e}")
    else:
      logger.error("CDP设置失败，无法使用Playwright")

  async def example_playwright_automation(self):
    """示例：使用Playwright连接到远程Chrome并进行自动化操作"""
    try:
      # 确保已经设置了CDP
      if not self.cdp_ws_endpoint:
        self.cdp_ws_endpoint = self.get_cdp_info_for_playwright()

      if not self.cdp_ws_endpoint:
        logger.error("未找到可用的WebSocket端点，无法使用Playwright连接")
        return False

      # 这里需要安装playwright: pip install playwright
      try:
        from playwright.async_api import async_playwright
      except ImportError:
        logger.error("请先安装playwright: pip install playwright")
        return False

      logger.info("使用Playwright连接到远程Chrome...")

      async with async_playwright() as p:
        # 连接到远程Chrome
        browser = await p.chromium.connect_over_cdp(self.cdp_ws_endpoint)
        logger.info("成功连接到远程Chrome")

        # 获取默认上下文和页面
        default_context = browser.contexts[0]
        pages = default_context.pages

        if not pages:
          logger.warning("没有找到打开的页面，创建新页面")
          page = await default_context.new_page()
        else:
          page = pages[0]
          logger.info(f"使用现有页面: {await page.title()}")

        # 导航到百度
        logger.info("导航到百度...")
        await page.goto("https://www.baidu.com")
        logger.info(f"页面标题: {await page.title()}")

        # 在搜索框中输入文字
        await page.fill("#kw", "Playwright自动化测试")

        # 点击搜索按钮
        await page.click("#su")

        # 等待搜索结果加载
        await page.wait_for_load_state("networkidle")

        # 截图保存
        screenshot_path = "/tmp/search_results.png"
        await page.screenshot(path=screenshot_path)
        logger.info(f"截图已保存到: {screenshot_path}")

        # 关闭浏览器连接
        await browser.close()
        logger.info("Playwright自动化示例完成")

        return True
    except Exception as e:
      logger.error(f"Playwright自动化失败: {e}")
      return False

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

      # 获取可用的调试目标
      ws_endpoint = self.get_available_cdp_targets()
      if ws_endpoint:
        self.cdp_ws_endpoint = ws_endpoint

      return True
    except Exception as e:
      logger.error(f"设置Chrome远程调试失败: {e}")
      return False

  def get_available_cdp_targets(self):
    """获取可用的CDP调试目标"""
    try:
      # 尝试获取可用的调试目标
      response = requests.get("http://localhost:9222/json", timeout=5)
      if response.status_code == 200:
        targets = response.json()
        if targets:
          logger.info(f"找到 {len(targets)} 个可用的调试目标:")
          for i, target in enumerate(targets):
            logger.info(f"目标 {i+1}: {target.get('title', 'Unknown')} - {target.get('type', 'Unknown')}")
            logger.info(f"  - URL: {target.get('url', 'Unknown')}")
            logger.info(f"  - WebSocket调试URL: {target.get('webSocketDebuggerUrl', 'Unknown')}")

          # 返回第一个可用的WebSocket URL，用于Playwright连接
          for target in targets:
            if target.get("type") == "page" and "webSocketDebuggerUrl" in target:
              logger.info(f"推荐使用的WebSocket URL: {target['webSocketDebuggerUrl']}")
              return target["webSocketDebuggerUrl"]
        else:
          logger.warning("没有找到可用的调试目标，请确保Chrome已正确启动")
      else:
        logger.warning(f"获取调试目标失败，状态码: {response.status_code}")
    except Exception as e:
      logger.warning(f"获取调试目标时出错: {e}")
    return None

  def get_cdp_info_for_playwright(self):
    """获取用于Playwright连接的CDP信息"""
    try:
      # 获取版本信息
      version_response = requests.get("http://localhost:9222/json/version", timeout=5)
      if version_response.status_code == 200:
        version_info = version_response.json()
        browser_ws_endpoint = version_info.get("webSocketDebuggerUrl")

        if browser_ws_endpoint:
          logger.info("Playwright连接信息:")
          logger.info(f"  - 浏览器WebSocket端点: {browser_ws_endpoint}")
          logger.info(f"  - 使用方法: playwright.chromium.connect(endpoint_url='{browser_ws_endpoint}')")
          return browser_ws_endpoint
        else:
          logger.warning("未找到WebSocket调试端点")
      else:
        logger.warning(f"获取版本信息失败，状态码: {version_response.status_code}")
    except Exception as e:
      logger.warning(f"获取Playwright连接信息时出错: {e}")
    return None
