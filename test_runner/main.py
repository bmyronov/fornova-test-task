import logging
import json

from time import sleep

from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException

from config import capabilities, appium_server_url, app_id
from handlers import TestRunner


# Configure logging
logger = logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%d-%m-%Y %H:%M:%S",
    # filename="./logs/basic.log", # Uncomment if you want to save logs to the log file.
)

# Create a logger for the main module
logger = logging.getLogger(__name__)


def get_driver() -> WebDriver:
    driver = webdriver.Remote(
        appium_server_url, options=UiAutomator2Options().load_capabilities(capabilities)
    )

    return driver


def main() -> None:
    print(appium_server_url)

    driver = get_driver()
    hotel_name: str = "The Grosvenor Hotel"
    app_test = TestRunner(app_id=app_id, driver=driver, hotel_name=hotel_name)

    date_list = [
        ["June 15", "June 16"],
        ["June 16", "June 17"],
        ["June 17", "June 18"],
        ["June 18", "June 19"],
        ["June 19", "June 26"],
    ]

    # Launch the app
    app_test.start_app()
    sleep(
        5
    )  # Time needed for the app to fully launch. You need to configure it yourself. It depends on phone specifications

    try:
        app_test.search_hotel()
    except NoSuchElementException:
        logger.error("No such element found")

    data = app_test.collect_data(date_list)
    data_json = json.dumps(data)
    logger.info(data_json)

    # Close the app
    app_test.close_app()


if __name__ == "__main__":
    main()
