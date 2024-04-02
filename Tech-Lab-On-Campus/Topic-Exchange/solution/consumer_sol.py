from consumer_interface import mqConsumerInterface
import pika
import os
import json


class mqConsumer(mqConsumerInterface):
    def __init__(self, exchange_name: str) -> None:
        # Save parameters to class variables
        self.exchange_name = exchange_name

        # Call setupRMQConnection
        self.setupRMQConnection()


    def setupRMQConnection(self) -> None:
        # Set-up Connection to RabbitMQ service
        con_params = pika.URLParameters(os.environ["AMQP_URL"])
        self.connection = pika.BlockingConnection(parameters=con_params)


        # Establish Channel
        self.channel = self.connection.channel()

        # Create the exchange if not already present
        exchange = self.channel.exchange_declare(exchange=self.exchange_name)

    def bindQueueToExchange(self, queueName: str, topic: str) -> None:
        # Bind Binding Key to Queue on the exchange
        self.channel.queue_bind(
            queue=queueName,
            routing_key=topic,
            exchange=self.exchange_name,
        )


    def createQueue(self, queueName: str) -> None:
        # Create Queue if not already present
        self.channel.queue_declare(queue=queueName)

        # Set-up Callback function for receiving messages
        self.channel.basic_consume(
            queue=queueName, on_message_callback=self.on_message_callback, auto_ack=False
        )


    def on_message_callback(self, channel, method_frame, header_frame, body):
        # De-Serialize JSON message object if Stock Object Sent
        message = json.loads(body)

        # Acknowledge And Print Message
        print(message)
        channel.basic_ack(delivery_tag=method_frame.delivery_tag)


    def startConsuming(self) -> None:
        # Start consuming messages
        self.channel.start_consuming()
