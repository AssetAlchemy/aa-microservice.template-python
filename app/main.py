import os
from dotenv import load_dotenv
import pika

# Load environment variables from .env file
load_dotenv(dotenv_path=".env", override=True)

# RabbitMQ environment variables
rabbitmq_host = os.getenv(key="RABBITMQ_HOST", default="rabbitmq")
rabbitmq_port = os.getenv(key="RABBITMQ_PORT", default="5672")
rabbitmq_user = os.getenv(key="RABBITMQ_USER", default="guest")
rabbitmq_password = os.getenv(key="RABBITMQ_PASSWORD", default="guest")
queue_name = os.getenv(key="RABBITMQ_QUEUE", default="test_queue")

# Connect to RabbitMQ
credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)
connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host=rabbitmq_host, port=rabbitmq_port, credentials=credentials
    )
)
channel = connection.channel()

# Declare a queue (ensures it exists)
channel.queue_declare(queue=queue_name)


# The callback function that is called when a new message arrives
def callback(ch, method, properties, body):
    print(f"New message: ch: {ch}")
    print(f"New message: method: {method}")
    print(f"New message: properties: {properties}")
    print(f"New message: body: {body.decode()}")


# Set up consumption of messages from the queue
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

print("Waiting for messages...")
channel.start_consuming()
