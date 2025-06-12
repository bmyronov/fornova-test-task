import uuid

from pika import ConnectionParameters, BlockingConnection, BasicProperties


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
