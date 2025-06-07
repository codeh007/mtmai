import logging

import uiautomator2 as u2
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

logger = logging.getLogger(__name__)


class InstBot:
  android_package_name = "com.instagram.android"
  android_apk_url = "https://apk2.yuepa8.com/apk/instgram_v2.apk"
  # 使用29222作为本地转发端口
  LOCAL_PORT = 29222

  def __init__(self, device_serial: str):
    self.device = u2.connect(device_serial)
    self.cdp_ws_endpoint = None
    # 设备主机名
    self.dev_host = device_serial.split(":")[0]
    self.driver = None

  async def install_apk(self):
    app_list = self.device.app_list()
    # 如果没安装就安装
    if self.android_package_name not in app_list:
      self.device.app_install(self.android_apk_url)

  async def start(self):
    # 如果没启动就启动
    logger.info("start inst bot")
    await self.install_apk()
    app_running_list = self.device.app_list_running()
    logger.info(f"app_running_list: {app_running_list}")
    if self.android_package_name not in app_running_list:
      self.device.app_start(self.android_package_name)
    else:
      logger.info(f"app {self.android_package_name} is already running")

    # 获取应用的登录UI 状态, 如果是登录框,就进行登录
    is_login_screen = self.device.xpath('//*[@content-desc="登入"]').exists
    await self.login()

  async def login(self):
    success = await self.open_android_chrome_with_cdp()
    if not success:
      logger.error("无法设置Chrome CDP")
      return False

    return await self.selenium_automation()

  async def selenium_automation(self):
    """使用Selenium连接到远程Chrome并进行简单的自动化操作"""
    try:
      logger.info(f"创建Selenium WebDriver连接到端口 {self.LOCAL_PORT}...")

      # 设置Chrome选项
      options = Options()
      # 连接到已经运行的Chrome实例
      options.add_experimental_option("debuggerAddress", f"localhost:{self.LOCAL_PORT}")

      # 创建WebDriver
      logger.info("初始化WebDriver...")
      self.driver = webdriver.Chrome(options=options)

      # 获取基本页面信息
      logger.info("获取当前页面信息...")
      current_url = self.driver.current_url
      page_title = self.driver.title

      logger.info(f"当前页面URL: {current_url}")
      logger.info(f"当前页面标题: {page_title}")

      # 获取页面源代码的前100个字符
      page_source = (
        self.driver.page_source[:100] + "..." if len(self.driver.page_source) > 100 else self.driver.page_source
      )
      logger.info(f"页面源代码预览: {page_source}")

      # 查找并显示页面上的链接数量
      links = self.driver.find_elements(By.TAG_NAME, "a")
      logger.info(f"页面上共有 {len(links)} 个链接")

      # 显示前5个链接的文本和URL
      for i, link in enumerate(links[:5]):
        link_text = link.text.strip() or "[无文本]"
        link_url = link.get_attribute("href") or "[无URL]"
        logger.info(f"链接 {i+1}: {link_text} - {link_url}")

      # 查找并显示页面上的图片数量
      images = self.driver.find_elements(By.TAG_NAME, "img")
      logger.info(f"页面上共有 {len(images)} 个图片")

      # 显示前3个图片的URL
      for i, img in enumerate(images[:3]):
        img_src = img.get_attribute("src") or "[无URL]"
        img_alt = img.get_attribute("alt") or "[无描述]"
        logger.info(f"图片 {i+1}: {img_alt} - {img_src}")

      # 获取网页窗口大小
      window_size = self.driver.get_window_size()
      logger.info(f"窗口大小: 宽={window_size['width']}px, 高={window_size['height']}px")

      # 获取页面Cookie
      cookies = self.driver.get_cookies()
      logger.info(f"页面Cookie数量: {len(cookies)}")

      # 执行简单的JavaScript获取页面加载时间
      load_time = self.driver.execute_script(
        "return (window.performance.timing.loadEventEnd - window.performance.timing.navigationStart) / 1000"
      )
      logger.info(f"页面加载时间: {load_time}秒")

      # 查找一个输入框
      try:
        input_elements = self.driver.find_elements(By.TAG_NAME, "input")
        if input_elements:
          logger.info(f"找到 {len(input_elements)} 个输入框")
          input_type = input_elements[0].get_attribute("type") or "[未指定]"
          input_id = input_elements[0].get_attribute("id") or "[无ID]"
          input_name = input_elements[0].get_attribute("name") or "[无名称]"
          logger.info(f"第一个输入框: ID={input_id}, 名称={input_name}, 类型={input_type}")
      except Exception as e:
        logger.warning(f"获取输入框信息时出错: {e}")

      logger.info("Selenium自动化操作成功完成")
      return True

    except Exception as e:
      logger.error(f"Selenium自动化操作失败: {e}")
      return False
    finally:
      # 断开连接但不关闭浏览器
      if self.driver:
        try:
          logger.info("断开WebDriver连接...")
          self.driver.quit()
        except Exception as e:
          logger.error(f"断开WebDriver连接时出错: {e}")
        self.driver = None

  async def backup_app_data(self):
    # 确保应用已关闭
    self.device.app_stop(self.android_package_name)
    # 使用 shell 命令执行备份
    self.device.shell("su -c 'tar -czf /sdcard/instagram_backup.tar.gz /data/data/com.instagram.android/'")
    # 将备份文件拉到电脑上
    # 这里需要使用 adb 命令，可以通过 subprocess 调用
