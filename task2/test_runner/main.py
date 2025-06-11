import logging
import json

from time import sleep

from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from config import capabilities, appium_server_url, app_id
from handlers import TestRunner


app = FastAPI()


# Configure logging
logger = logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%d-%m-%Y %H:%M:%S",
    # filename="./logs/basic.log",
)

# Create a logger for the main module
logger = logging.getLogger(__name__)


def get_driver() -> WebDriver:
    driver = webdriver.Remote(
        appium_server_url, options=UiAutomator2Options().load_capabilities(capabilities)
    )

    return driver


def main(hotel_name: str, date_list: list[list[str]]) -> dict[str, dict[str, str]]:
    print(appium_server_url)

    driver = get_driver()
    app_test = TestRunner(app_id=app_id, driver=driver, hotel_name=hotel_name)

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
    logger.info(data)

    # Close the app
    app_test.close_app()

    return data


@app.post("/search")
def search_hotel(params: dict[str, list[list[str]]]) -> JSONResponse:
    hotel_name, date_list = [[k, v] for k, v in params.items()][0]
    data = main(hotel_name, date_list)

    # data = {
    #     "The Grosvenor Hotel": {
    #         "June 15 - June 16": {
    #             "Tripadvisor": "$60",
    #             "Booking.com": "$59",
    #             "screenshot": "tripadvisor_The_Grosvenor_Hotel_June_15-June_16",
    #         },
    #         "June 16 - June 17": {
    #             "Tripadvisor": "$49",
    #             "Booking.com": "$49",
    #             "screenshot": "tripadvisor_The_Grosvenor_Hotel_June_16-June_17",
    #         },
    #         "June 17 - June 18": {
    #             "Tripadvisor": "$60",
    #             "Booking.com": "$59",
    #             "screenshot": "tripadvisor_The_Grosvenor_Hotel_June_17-June_18",
    #         },
    #         "June 18 - June 19": {
    #             "Tripadvisor": "$60",
    #             "Booking.com": "$59",
    #             "screenshot": "tripadvisor_The_Grosvenor_Hotel_June_18-June_19",
    #         },
    #         "June 19 - June 26": {
    #             "Tripadvisor": "$57",
    #             "Booking.com": "$57",
    #             "screenshot": "tripadvisor_The_Grosvenor_Hotel_June_19-June_26",
    #         },
    #     }
    # }

    return JSONResponse(content=jsonable_encoder(data))
