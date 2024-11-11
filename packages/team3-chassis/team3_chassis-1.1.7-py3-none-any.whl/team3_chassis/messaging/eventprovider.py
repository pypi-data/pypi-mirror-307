import asyncio
import logging.config
import os

import aio_pika
from aio_pika import IncomingMessage, ExchangeType


class EventProvider:

    connection: aio_pika.robust_connection = None
    channel : aio_pika.channel= None
    exchange_name = None
    exchange : aio_pika.robust_exchange = None
    rabbitmq_host = None
    rabbitmq_user = None
    rabbitmq_password = None
    logger : logging.Logger = None

    @classmethod
    async def create(cls,rabbitmq_host, rabbitmq_user, rabbitmq_password, logger: logging.Logger, exchange_name:str='events'):
        self=EventProvider()
        self.rabbitmq_host = rabbitmq_host
        self.rabbitmq_user = rabbitmq_user
        self.rabbitmq_password = rabbitmq_password
        self.logger = logger
        self.exchange_name = exchange_name
        await self.subscribe_channel(exchange_name)
        return self


    async def subscribe_channel(self, exchange_name):
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
        self.logger.info("Exchange created")
        self.exchange = await self.channel.declare_exchange(name=exchange_name, type=ExchangeType.TOPIC, durable=True)

    async def subscribe_to_service(self, queue_name:str, routing_key:str,callback: callable([IncomingMessage])):
        # Create a queue
        queue = await self.channel.declare_queue(name=queue_name, exclusive=True)
        # Bind the queue to the exchange
        await queue.bind(exchange=self.exchange_name, routing_key=routing_key)
        # Set up a message consumer
        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                self.logger.info("Received message en event service order.payed" )
                await callback(message)

    async def publish(self,message_body, routing_key):
        # Publish the message to the exchange
        self.logger.info("Publishing message to exchange %s with routing key %s", self.exchange_name, routing_key)
        await self.exchange.publish(
            aio_pika.Message(
                body=message_body.encode(),
                content_type="text/plain"
            ),
            routing_key=routing_key)

    async def publish_to_exchange(self, message, routing_key, exchange_name):
        await self.subscribe_channel(exchange_name)
        self.logger.info("Sending log to exchange %s with routing key %s", exchange_name, routing_key)
        await self.publish(message, routing_key)
    
        