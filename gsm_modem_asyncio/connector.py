class Connector:

    def __init__(self, client, serial_url, baudrate):
        self.client = client
        self.serial_url = serial_url
        self.baudrate = baudrate
        self.ready = False

    async def connect(self):
        raise NotImplementedError

    async def close(self):
        raise NotImplementedError

    async def send(self, data):
        raise NotImplementedError

    async def ensure(self):
        if self.ready:
            return
        await self.connect()
