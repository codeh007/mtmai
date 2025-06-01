import logging
from urllib.parse import urlparse

import adbutils

logger = logging.getLogger(__name__)


class InstagramAutomation:
  def __init__(self, endpoint: str):
    uri = urlparse(endpoint)
    self.host = uri.hostname
    self.port = uri.port
    if not self.host or not self.port:
      raise ValueError("InstagramAutomation Invalid endpoint")
    logger.info(f"Connecting to {self.host}:{self.port}")
    # Initialize ADB client to connect to local ADB server (which runs on 5037)
    self.adb = adbutils.AdbClient(host="127.0.0.1", port=5037)

  async def start(self):
    await self.open_clash()

  async def open_clash(self):
    logger.info("Connecting to adb")
    try:
      # Connect to the device using device serial (host:port format)
      device_serial = f"{self.host}:5555"  # 使用5555端口连接设备

      # First ensure the device is connected via ADB
      logger.info(f"Attempting to connect to device: {device_serial}")
      connection_result = self.adb.connect(device_serial)
      logger.info(f"ADB connect result: {connection_result}")

      # Get the device object
      device = self.adb.device(serial=device_serial)

      if not device:
        raise Exception(f"Failed to connect to device {device_serial}")

      logger.info(f"Successfully connected to device {device_serial}")

      # List all connected devices with detailed information
      logger.info("Connected devices:")
      devices = self.adb.device_list()
      if not devices:
        logger.warning("No devices found!")

      for info in devices:
        logger.info(f"Device: {info.serial}")

      return device

    except Exception as e:
      logger.error(f"Failed to connect to ADB: {str(e)}")
      raise
