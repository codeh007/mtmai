# Python/Pytest
import pytest
from appium import webdriver

# Options are only available since client version 2.3.0
# If you use an older client then switch to desired_capabilities
# instead: https://github.com/appium/python-client/pull/720
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions
from appium.webdriver.appium_service import AppiumService
from appium.webdriver.common.appiumby import AppiumBy

APPIUM_PORT = 4724
APPIUM_HOST = "100.117.139.87"


# HINT: fixtures below could be extracted into conftest.py
# HINT: and shared across all tests in the suite
@pytest.fixture(scope="session")
def appium_service():
  service = AppiumService()
  service.start(
    # Check the output of `appium server --help` for the complete list of
    # server command line arguments
    args=["--address", APPIUM_HOST, "-p", str(APPIUM_PORT)],
    timeout_ms=20000,
  )
  yield service
  service.stop()


def create_ios_driver(custom_opts=None):
  options = XCUITestOptions()
  options.platformVersion = "13.4"
  options.udid = "123456789ABC"
  if custom_opts is not None:
    options.load_capabilities(custom_opts)
  # Appium1 points to http://127.0.0.1:4723/wd/hub by default
  return webdriver.Remote(f"http://{APPIUM_HOST}:{APPIUM_PORT}", options=options)


def create_android_driver(custom_opts=None):
  options = UiAutomator2Options()
  options.platformVersion = "10"
  options.udid = "123456789ABC"
  if custom_opts is not None:
    options.load_capabilities(custom_opts)
  # Appium1 points to http://127.0.0.1:4723/wd/hub by default
  return webdriver.Remote(f"http://{APPIUM_HOST}:{APPIUM_PORT}", options=options)


@pytest.fixture
def ios_driver_factory():
  return create_ios_driver


@pytest.fixture
def ios_driver():
  # prefer this fixture if there is no need to customize driver options in tests
  driver = create_ios_driver()
  yield driver
  driver.quit()


@pytest.fixture
def android_driver_factory():
  return create_android_driver


@pytest.fixture
def android_driver():
  # prefer this fixture if there is no need to customize driver options in tests
  driver = create_android_driver()
  yield driver
  driver.quit()


def test_ios_click(appium_service, ios_driver_factory):
  # Usage of the context manager ensures the driver session is closed properly
  # after the test completes. Otherwise, make sure to call `driver.quit()` on teardown.
  with ios_driver_factory({"appium:app": "/path/to/app/UICatalog.app.zip"}) as driver:
    el = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="item")
    el.click()


def test_android_click(appium_service, android_driver_factory):
  # Usage of the context manager ensures the driver session is closed properly
  # after the test completes. Otherwise, make sure to call `driver.quit()` on teardown.
  with android_driver_factory(
    {
      "appium:app": "/path/to/app/test-app.apk",
      "appium:udid": "567890",
    }
  ) as driver:
    el = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="item")
    el.click()
