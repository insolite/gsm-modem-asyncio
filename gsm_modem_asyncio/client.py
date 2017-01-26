class Client:

    def __init__(self, connector_factory, args, kwargs):
        super().__init__()
        self.connector_factory = connector_factory
        self.args = args
        self.kwargs = kwargs
        self.connector = None

    async def connect(self):
        if not self.connector:
            self.connector = self.connector_factory(self, *self.args, **self.kwargs)
        await self.connector.connect()

    async def close(self):
        if self.connector:
            await self.connector.close()
        self.connector = None

    async def ensure(self):
        if not self.connector:
            await self.connect()
        await self.connector.ensure()

    async def send(self, data):
        await self.connector.send(data)

    async def send_text(self, text):
        await self.send(text.encode())
