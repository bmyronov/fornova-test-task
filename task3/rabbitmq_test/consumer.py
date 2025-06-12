import sys
import os
import json

from pika import ConnectionParameters, BlockingConnection, BasicProperties

connection_params = ConnectionParameters(host="localhost", port=5672)
connection = BlockingConnection(connection_params)
channel = connection.channel()


def get_hotel_result(query: str) -> str:
    print(query)

    data = {
        "The Grosvenor Hotel": {
            "June 15 - June 16": {
                "Tripadvisor": "$60",
                "Booking.com": "$59",
                "screenshot": "tripadvisor_The_Grosvenor_Hotel_June_15-June_16.png",
            },
            "June 16 - June 17": {
                "Tripadvisor": "$58",
                "Booking.com": "$49",
                "screenshot": "tripadvisor_The_Grosvenor_Hotel_June_16-June_17.png",
            },
            "June 17 - June 18": {
                "Tripadvisor": "$71",
                "Booking.com": "$59",
                "screenshot": "tripadvisor_The_Grosvenor_Hotel_June_17-June_18.png",
            },
            "June 18 - June 19": {
                "Tripadvisor": "$60",
                "Booking.com": "$59",
                "screenshot": "tripadvisor_The_Grosvenor_Hotel_June_18-June_19.png",
            },
            "June 19 - June 26": {
                "Tripadvisor": "$57",
                "Booking.com": "$57",
                "screenshot": "tripadvisor_The_Grosvenor_Hotel_June_19-June_26.png",
            },
        }
    }

    return json.dumps(data)


def on_request(ch, method, props, body):
    # n = int(body)

    # print(f" [.] fib({n})")
    # response = fib(n)

    print(body)
    response = get_hotel_result(body)

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
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
