import pytest

from appium import webdriver
from appium.options.android import UiAutomator2Options

# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

from config import capabilities, appium_server_url, app_id
from handlers import AppTest


def main() -> None:
    print(appium_server_url)

    driver = webdriver.Remote(
        appium_server_url, options=UiAutomator2Options().load_capabilities(capabilities)
    )

    app_test = AppTest(app_id=app_id, driver=driver)
    hotel_name: str = "The Grosvenor Hotel"
    try:
        app_test.search_hotel(hotel_name)
    except NoSuchElementException:
        app_test.search_hotel(hotel_name)

    date_list = [
        ["June 15", "June 16"],
        ["June 16", "June 17"],
        ["June 17", "June 18"],
        ["June 18", "June 19"],
        ["June 19", "June 26"],
    ]
    app_test.collect_data(date_list)


if __name__ == "__main__":
    main()
