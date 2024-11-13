import json

import pika

from config.envs import (
    rabbitmq_user,
    rabbitmq_password,
    rabbitmq_host,
    rabbitmq_port,
    exchange,
    queue_name,
    queue_name_send,
)
from entities.message import (
    MessageRecieved,
    MessageToSend,
    MessageErrorToSend,
    MissingFieldError,
)
from database import get_file, upload_file, FileNotFound


# Connect to RabbitMQ
def init_broker():
    credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=rabbitmq_host, port=rabbitmq_port, credentials=credentials
        )
    )
    channel = connection.channel()

    # Config chanel
    channel.exchange_declare(exchange=exchange, durable=True)
    channel.queue_declare(queue=queue_name, durable=True)
    channel.queue_bind(queue=queue_name, exchange=exchange)

    # Set up consumption of messages from the queue
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    channel.start_consuming()


def send_message(message_body):
    """Send a message to the 'queue_name_send' queue"""
    credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=rabbitmq_host, port=rabbitmq_port, credentials=credentials
        )
    )
    channel = connection.channel()

    # Declare the exchange and queue (same as in init_broker)
    channel.exchange_declare(exchange=exchange, durable=True)
    channel.queue_declare(queue=queue_name_send, durable=True)
    channel.queue_bind(
        queue=queue_name_send, exchange=exchange, routing_key=queue_name_send
    )

    # Send the message
    channel.basic_publish(
        exchange=exchange,
        routing_key=queue_name_send,
        body=str(message_body),
        properties=pika.BasicProperties(
            delivery_mode=2,  # Make the message persistent
        ),
    )

    # Close the connection
    connection.close()


# The callback function that is called when a new message arrives
def callback(ch, method, properties, body):
    try:
        print(f"New message: ch: {ch}")
        print(f"New message: method: {method}")
        print(f"New message: properties: {properties}")
        print(f"New message: body: {body.decode()}")

        message = MessageRecieved(message_dict=json.loads(body.decode("utf-8")))
        file = get_file(message.asset_id)
        # HERE YOU CAN MAKE YOUR OWN TRANSFORMATION
        new_file_id = upload_file(file)
        send_message(
            MessageToSend(
                message_dict={
                    "message_version": getattr(message, "message_version", None),
                    "trace_id": getattr(message, "trace_id", None),
                    "asset_id": new_file_id,
                }
            ).to_dict()
        )

    except json.JSONDecodeError:
        send_message(
            MessageErrorToSend(
                message_dict={
                    "message_version": 1.0,
                    "trace_id": 0,
                    "asset_id": 0,
                    "error": "Error to parse message",
                    "options": {},
                }
            ).to_dict()
        )

    except (MissingFieldError, FileNotFound) as e:
        message = MessageRecieved(
            message_dict=json.loads(body.decode("utf-8"))
        ).to_dict()

        send_message(
            MessageErrorToSend(
                message_dict={
                    "message_version": getattr(message, "message_version", None),
                    "trace_id": getattr(message, "trace_id", None),
                    "asset_id": getattr(message, "asset_id", None),
                    "error": str(e),
                    "options": getattr(message, "options", {}),
                }
            ).to_dict()
        )
