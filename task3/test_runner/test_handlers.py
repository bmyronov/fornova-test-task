import pytest

from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException

from config import capabilities, appium_server_url, app_id
from handlers import TestRunner


driver = webdriver.Remote(
    appium_server_url, options=UiAutomator2Options().load_capabilities(capabilities)
)
app_test = TestRunner(driver=driver, app_id=app_id, hotel_name="The Grosvenor Hotel")


@pytest.fixture()
def start_app() -> None:
    app_test.start_app()
