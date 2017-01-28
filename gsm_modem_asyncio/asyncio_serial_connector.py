import asyncio

import serial_asyncio

from .connector import Connector
from .serial_protocol import SerialProtocol


class AsyncioSerialConnector(Connector):

    def __init__(self, client, serial_url, baudrate):
        super().__init__(client, serial_url, baudrate)
        self.protocol = None
        self.connection_future = None

    async def connect(self):
        _, self.protocol = await serial_asyncio.create_serial_connection(
            asyncio.get_event_loop(),
            lambda: SerialProtocol(self),
            self.serial_url,
            baudrate=self.baudrate
        )
        self.ready = True
        self.connection_future = asyncio.Future()
        await self.connection_future

    async def close(self):
        if self.protocol:
            self.protocol.close()
        self.protocol = None
        self.ready = False

    async def send(self, data):
        self.protocol.send(data)

    def got_data(self, data):
        self.client.got_data(data)

    def connected(self):
        self.connection_future.set_result(None)
