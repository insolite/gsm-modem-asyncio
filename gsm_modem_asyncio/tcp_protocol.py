import asyncio


class TcpProtocol(asyncio.Protocol):

    def __init__(self):
        super().__init__()
        self.transport = None
        self.connection_lost_future = asyncio.Future()

    def connection_made(self, transport):
        super().connection_made(transport)
        self.transport = transport
        if self.connection_lost_future.done():
            self.connection_lost_future = asyncio.Future()

    def connection_lost(self, exc):
        super().connection_lost(exc)
        self.transport = None
        if not self.connection_lost_future.done():
            self.connection_lost_future.set_result(None)

    def send(self, data):
        self.transport.write(data)

    def close(self):
        if self.transport:
            self.transport.close()
            self.transport = None

    async def wait_disconnect(self):
        await self.connection_lost_future
