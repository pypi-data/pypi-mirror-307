import asyncio
import json
import logging.config
import aio_pika
from aio_pika import ExchangeType

class LoggerProvider:

    connection: aio_pika.robust_connection = None
    channel : aio_pika.channel= None
    exchange_name = None
    exchange : aio_pika.robust_exchange = None
    rabbitmq_host = None
    rabbitmq_user = None
    rabbitmq_password = None
    logger : logging.Logger = None

    @classmethod
    async def create(cls,rabbitmq_host, rabbitmq_user, rabbitmq_password, logger: logging.Logger):
        self=LoggerProvider()
        self.rabbitmq_host = rabbitmq_host
        self.rabbitmq_user = rabbitmq_user
        self.rabbitmq_password = rabbitmq_password
        self.logger = logger
        await self.subscribe_channel()
        return self


    async def subscribe_channel(self):
        retries = 5
        for attempt in range(retries):
            try:
                self.connection = await aio_pika.connect_robust(
                    host=self.rabbitmq_host,
                    virtualhost='/',
                    login=self.rabbitmq_user,
                    password=self.rabbitmq_password
                )
            except Exception as e:
                self.logger.error(f"Connection failed: {e}")
                if attempt < retries - 1:
                    self.logger.info(f"Retrying in {5} seconds...")
                    await asyncio.sleep(5)
                else:
                    self.logger.error("All retry attempts failed")
                    raise e
        self.logger.info("Connection established")
        # Create a channel
        self.logger.info("Connected to RabbitMQ")
        self.channel = await self.connection.channel()
        self.logger.info("Channel created")
        self.exchange_name = 'events'
        self.logger.info("Exchange created")
        self.exchange = await self.channel.declare_exchange(name=self.exchange_name, type=ExchangeType.TOPIC, durable=True)


    async def send_log(self, key,message, routing_key):
        data={
            "key": key,
            "message": message
        }
        message_body = json.dumps(data)
        await self.publish(message_body, routing_key)

    async def publish(self,message_body, routing_key):
        # Publish the message to the exchange
        self.logger.info("Publishing message to exchange %s with routing key %s", self.exchange_name, routing_key)
        await self.exchange.publish(
            aio_pika.Message(
                body=message_body.encode(),
                content_type="text/plain"
            ),
            routing_key=routing_key)