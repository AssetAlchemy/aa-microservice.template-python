import json
import uuid
import datetime

import pika
import pika.spec

from config.envs import (
    rabbitmq_user,
    rabbitmq_password,
    rabbitmq_host,
    rabbitmq_port,
    exchange,
    queue_name,
    queue_name_send,
    source,
)
from database import get_file, upload_file, GetFileError, UploadFileError, FileNotFound


# Connect to RabbitMQ
def init_broker():
    credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=rabbitmq_host, port=rabbitmq_port, credentials=credentials
        )
    )
    channel = connection.channel()

    # Set up consumption of messages from the queue
    channel.basic_consume(queue=queue_name, on_message_callback=callback)
    channel.start_consuming()


def send_message(message_body, correlation_id):
    """Send a message to the 'queue_name_send' queue"""
    credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=rabbitmq_host, port=rabbitmq_port, credentials=credentials
        )
    )
    channel = connection.channel()

    # Declare the exchange and queue (same as in init_broker)
    channel.queue_bind(
        queue=queue_name_send, exchange=exchange, routing_key=queue_name_send
    )

    channel.basic_publish(
        exchange=exchange,
        routing_key=queue_name_send,
        body=json.dumps(message_body),
        properties=pika.BasicProperties(
            delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE,
            app_id=source,
            content_type="application/json",
            message_id=str(uuid.uuid4()),
            timestamp=int(datetime.datetime.now().timestamp()),
            correlation_id=correlation_id,
        ),
    )
    connection.close()


# The callback function that is called when a new message arrives
def callback(channel, method, properties, body):
    try:
        message = json.loads(body.decode("utf-8"))

        try:
            file = get_file(message.get("asset_id", None))
            # HERE YOU CAN MAKE YOUR TRANSFORMATION
            new_file_id = upload_file(file)
            send_message(
                message_body={
                    "asset_id": new_file_id,
                    "options": getattr(message, "options", {}),
                    "status": "normal",
                },
                correlation_id=properties.correlation_id,
            )
            channel.basic_ack(delivery_tag=method.delivery_tag)

        except (GetFileError, UploadFileError, FileNotFound, Exception) as e:
            print(e)
            send_message(
                message_body={
                    "asset_id": str(getattr(e, "file_id", 0)),
                    "options": getattr(message, "options", {}),
                    "status": "error",
                    "error": str(e),
                },
                correlation_id=properties.correlation_id,
            )
            channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

    except json.JSONDecodeError:
        print("Error to parse message")
        channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
