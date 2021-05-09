import asyncio
from typing import Union

import aiormq

from aiormq import connection
from aiormq import channel

from utils import singleton


class Connector(metaclass=singleton.Singleton):
    def __init__(self, host="localhost", port=5675,
                 user="guest", password="guest"):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        # connection = await aio_pika.connect_robust("amqp://guest:guest@127.0.0.1/")

        self._connection: Union[connection.Connection, None] = None
        self._connection_is_creating = False

        self._channel: Union[channel.Channel, None] = None
        self._channel_is_creating = False

    async def get_connection(self) -> connection.Connection:
        while self._connection_is_creating and \
                (self._connection is None or self._connection.is_closed):
            await asyncio.sleep(0.1)
        if self._connection is None or self._connection.is_closed:
            print("Create new connection")
            self._connection_is_creating = True
            self._connection = await aiormq.connect(
                f"amqp://{self.user}:{self.password}@{self.host}:{self.port}/"
            )
            self._connection_is_creating = False
        return self._connection

    async def get_channel(self) -> channel.Channel:
        conn = await self.get_connection()
        while self._channel_is_creating and \
                (self._channel is None or self._channel.is_closed):
            await asyncio.sleep(0.1)
        if self._channel is None or self._channel.is_closed:
            print("creating new channel")
            self._channel_is_creating = True
            self._channel = await conn.channel()
            self._channel_is_creating = False
        return self._channel
