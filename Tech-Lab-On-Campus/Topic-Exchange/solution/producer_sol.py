""" from producer_interface import mqProducerInterface
import pika
import os


class mqProducer(mqProducerInterface):
    def __init__(self, routing_key: str, exchange_name: str) -> None:
        # Save parameters to class variables
        self.routing_key = routing_key
        self.exchange_name = exchange_name
        

        # Call setupRMQConnection
        self.setupRMQConnection()

    def setupRMQConnection(self) -> None:
        # Set-up Connection to RabbitMQ service
        con_params = pika.URLParameters(os.environ["AMQP_URL"])
        self.connection = pika.BlockingConnection(parameters=con_params)

        # Establish Channel
        self.channel = self.connection.channel()

        self.channel.exchange_declare(exchange=self.exchange_name, exhange_type="topic")


    def publishOrder(self, message: str) -> None:
        # Create Appropiate Topic String

        # Send serialized message or String
        self.channel.basic_publish(exchange=self.exchange_name, routing_key=self.routing_key, body=message)

        # Print Confirmation
        print(f"Sent message to {self.routing_key}")

        # Close channel and connection
        self.channel.close()
        self.connection.close()


 """

from producer_interface import mqProducerInterface
import pika
import os


# Constructor: Call the setupRMQConnection function.
# setupRMQConnection Function: Establish connection to the RabbitMQ service.
# publishOrder:  Publish a simple UTF-8 string message from the parameter.
# publishOrder:  Close Channel and Connection.  

class mqProducer(mqProducerInterface):
    # Constructor: Call the setupRMQConnection function.
    def __init__(self, routing_key: str, exchange_name: str) -> None:
        # Save parameters to class variables
        self.routing_key = routing_key
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
        exchange = self.channel.exchange_declare(exchange=self.exchange_name, exchange_type="topic")


    def publishOrder(self, message: str) -> None:
        # Basic Publish to Exchange
        self.channel.basic_publish(
            exchange=self.exchange_name,
            routing_key=self.routing_key,
            body=message,
        )

        # Close Channel
        self.channel.close()

        # Close Connection
        self.connection.close()