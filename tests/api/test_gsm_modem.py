from gsm_modem_asyncio import GsmModem
from tests.common import GsmSerialTest


SERIAL_URL = '/dev/ttyS0'
PHONE_NUMBER = ''


class GsmModemTest(GsmSerialTest):

    def setUp(self):
        super().setUp()
        self.gsm_modem = GsmModem(SERIAL_URL)
        self.loop.run_until_complete(self.gsm_modem.connect())

    def test_get_csq(self):
        csq = self.loop.run_until_complete(
            self.gsm_modem.get_csq()
        )

        self.assertIsInstance(csq, int)
        print(csq)

    def test_send_ussd(self):
        reply = self.loop.run_until_complete(
            self.gsm_modem.send_ussd('*111#')
        )

        self.assertIsInstance(reply, str)
        print(reply)

    def test_call(self):
        self.loop.run_until_complete(
            self.gsm_modem.call(PHONE_NUMBER, 20)
        )

    def test_send_sms(self):
        self.loop.run_until_complete(
            self.gsm_modem.send_sms(PHONE_NUMBER, 'Hello world')
        )
