import asyncio
import re

from .regexp_client import RegexpClient
from .asyncio_serial_connector import AsyncioSerialConnector
from .exceptions import (
    NoReplyAtError,
    CallError,
    CsqError,
    NoReplySmsError,
    UnexpectedReplySmsError,
    NoReplyUssdError,
    UnexpectedReplyUssdError,
    DeviceUssdError,
    OperationNotSupportedUssdError,
)


def at_operation(func):
    async def wrapped(self, *args, **kwargs):
        with await self.operation_lock:
            await self.ensure()
            try:
                return await func(self, *args, **kwargs)
            except asyncio.CancelledError:
                raise NoReplyAtError
    return wrapped


class GsmModem(RegexpClient):

    def __init__(self, serial_url, baudrate=9600, line_end='\r\n', connector_factory=AsyncioSerialConnector):
        super().__init__(connector_factory, (serial_url, baudrate))
        self.serial_url = serial_url
        self.baudrate = baudrate
        self.line_end = line_end
        self.operation_lock = asyncio.Lock()

    @property
    def ready(self):
        return self.connector.ready if self.connector else False

    def get_line(self, cmd):
        return '{}{}'.format(cmd, self.line_end)

    async def send_line(self, text):
        await self.send_text(self.get_line(text))

    async def send_cmd(self, cmd, timeout, *reply_templates):
        cmdf = self.get_line(cmd)
        await self.send_text(cmdf)
        index, match = await self.get_line_reply(5, re.escape(cmdf))
        if reply_templates:
            return await self.get_line_reply(timeout, *reply_templates)
        return index, match

    async def get_line_reply(self, timeout, *reply_templates):
        return await self.get_reply(
            timeout,
            *[self.get_line(reply_template)
              for reply_template in reply_templates]
        )

    @at_operation
    async def call(self, number, seconds):
        call_cmd = 'ATD{};'.format(number)
        await self.send_line(call_cmd)
        atd_templates = (r'NO DIALTONE', r'BUSY', r'NO CARRIER', r'NO ANSWER')
        index, match = await self.get_line_reply(10, r'OK', r'ERROR', *atd_templates)
        if index != 0:
            raise CallError
        try:
            await self.get_line_reply(seconds, *atd_templates)
        except asyncio.CancelledError:
            await self.send_line('ATH')
            index, match = await self.get_line_reply(10, r'OK', r'ERROR')
            if index != 0:
                raise CallError

    @at_operation
    async def get_csq(self):
        csq_cmd = 'AT+CSQ'
        match_index, match = await self.send_cmd(csq_cmd, 5, r'\+CSQ:\s*(\d+)(,\d+)?', r'ERROR')
        if match_index == 0:
            await self.get_line_reply(5, r'OK')
            csq = int(match.group(1))
        else:
            raise CsqError
        return csq

    @at_operation
    async def send_ussd(self, cmd, timeout=20, end_session=True):
        ussd_cmd = 'AT+CUSD=1,"{}"'.format(cmd)
        await self.send_line(ussd_cmd)
        try:
            await self.get_line_reply(5, r'OK')
        except asyncio.CancelledError:
            raise NoReplyUssdError
        try:
            match_index, match = await self.get_line_reply(timeout, r'\+CUSD:\s*(\d+),"(.*)",\s*(\d+)', r'\+CUSD:\s*4.*')
        except asyncio.CancelledError:
            if self.buffer:
                raise UnexpectedReplyUssdError
            raise NoReplyUssdError
        if match_index == 0:
            return match.group(2).replace('\r\n', '')
        elif match_index == 1:
            raise OperationNotSupportedUssdError
        raise DeviceUssdError

    @at_operation
    async def send_sms(self, number, text, timeout=20, cmgf=1):
        try:
            # CMGF
            match_index, match = await self.send_cmd('AT+CMGF={}'.format(cmgf), 5, r'OK')
            if match_index != 0:
                raise UnexpectedReplySmsError
            # CNMI
            match_index, match = await self.send_cmd('AT+CNMI=2,1,0,0,0', 5, r'OK')
            if match_index != 0:
                raise UnexpectedReplySmsError
            # CMGS
            await self.send_cmd('AT+CMGS="{}"'.format(number), 5)
            match_index, match = await self.get_reply(5, r'>', r'ERROR\r\n')
            if match_index != 0:
                raise UnexpectedReplySmsError
            # text
            try:
                match_index, match = await self.send_cmd(text, 5)
                if match_index != 0:
                    raise UnexpectedReplySmsError
            finally:
                await self.send_text('\x1a')
            match_index, match = await self.get_line_reply(timeout, r'\+CMGS:\s*(\d+)', r'ERROR')
            if match_index != 0:
                raise UnexpectedReplySmsError
            await self.get_line_reply(5, r'OK')
        except asyncio.CancelledError:
            if self.buffer:
                raise UnexpectedReplySmsError
            raise NoReplySmsError
