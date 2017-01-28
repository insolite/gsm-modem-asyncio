from structlog import get_logger

from .tcp_protocol import TcpProtocol


class SerialProtocol(TcpProtocol):

    def __init__(self, connector):
        super().__init__()
        self.connector = connector
        self.logger = get_logger()

    def send(self, data):
        super().send(data)
        self.logger.debug('serial_-->', data=data)

    def connection_made(self, transport):
        super().connection_made(transport)
        transport.serial.rts = False  # You can manipulate Serial object via transport
        self.connector.connected()

    def data_received(self, data):
        super().data_received(data)
        self.logger.debug('serial_<--', data=data)
        self.connector.got_data(data)

    def connection_lost(self, exc):
        super().connection_lost(exc)
