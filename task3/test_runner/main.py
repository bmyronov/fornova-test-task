import logging
import json

from typing import Any
from time import sleep

from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException
from pika import ConnectionParameters, BlockingConnection, BasicProperties

from config import capabilities, appium_server_url, app_id, RABBITMQ_HOST, RABBITMQ_PORT
from handlers import TestRunner

# Configure logging
logger = logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%d-%m-%Y %H:%M:%S",
    # filename="./logs/basic.log",
)

# Create a logger for the main module
logger = logging.getLogger(__name__)

connection_params = ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT)
connection = BlockingConnection(connection_params)
channel = connection.channel()


def get_driver() -> WebDriver:
    driver = webdriver.Remote(
        appium_server_url, options=UiAutomator2Options().load_capabilities(capabilities)
    )

    return driver


def get_hotel_result(hotel_name: str, date_list: list[list[str]]) -> dict[str, Any]:
    logger.info(f"Appium server url: {appium_server_url}")

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


def on_request(ch, method, props, body):
    query = json.loads(body)
    query_items: list[list[str | list[str]]] = [[k, v] for k, v in query.items()]
    hotel_name: str = query_items[0][0]
    date_list: list[list[str]] = query_items[0][1]
    response = json.dumps(get_hotel_result(hotel_name, date_list))
    logger.info(response)

    ch.basic_publish(
        exchange="",
        routing_key=props.reply_to,
        properties=BasicProperties(correlation_id=props.correlation_id),
        body=response,
    )
    ch.basic_ack(delivery_tag=method.delivery_tag)


def main() -> None:
    channel.queue_declare(queue="hotel_result")
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(
        queue="hotel_result", auto_ack=False, on_message_callback=on_request
    )

    print(" [x] Awaiting RPC requests")
    channel.start_consuming()


if __name__ == "__main__":
    main()
