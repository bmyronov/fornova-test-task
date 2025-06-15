import uuid
import logging
import json

from pika import ConnectionParameters, BlockingConnection, BasicProperties

from config import RABBITMQ_HOST, RABBITMQ_PORT
from crud import create_result

# Create a logger for this module
logger = logging.getLogger(__name__)

connection_params = ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT)


class HotelResult(object):
    def __init__(self, connection_params: ConnectionParameters):
        self.connection = BlockingConnection(connection_params)
        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue="", exclusive=True, durable=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True,
        )

        self.response = None
        self.corr_id = None

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, query):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange="",
            routing_key="hotel_result",
            properties=BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=str(query),
        )
        while self.response is None:
            self.connection.process_data_events(time_limit=None)
        return self.response


def get_message(query: dict[str, list[list[str]]]) -> None:
    if not query:
        logger.error("Query is empty!")

    query = json.dumps(query)

    hotel_result = HotelResult(connection_params=connection_params)
    response: str | None = hotel_result.call(query)

    # Add response to db if exists
    if response:
        create_result(response)

    return response
