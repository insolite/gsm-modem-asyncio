import asyncio
import re

from structlog import get_logger

from .client import Client


class TimeoutFuture(asyncio.Future):

    def __init__(self, timeout):
        super().__init__()
        if not timeout is None:
            asyncio.get_event_loop().call_later(timeout, self.cancel)


class ReplyFuture(TimeoutFuture):
    def __init__(self, timeout=5, reply_templates=None):
        super().__init__(timeout)
        self.reply_templates = reply_templates


class RegexpClient(Client):

    def __init__(self, connector_factory, args=(), kwargs={}):
        super().__init__(connector_factory, args, kwargs)
        self.buffer = ''
        self.reply_future = None
        self.logger = get_logger()

    def got_data(self, data):
        new_data = data.decode(errors='replace')
        self.buffer += new_data
        self.logger.debug('buffer_append', buffer=self.buffer)
        if self.reply_future and not self.reply_future.done():
            self.check_msg()

    def check_msg(self):
        for index, reply_template in enumerate(self.reply_future.reply_templates):
            match = re.search(reply_template, self.buffer, re.DOTALL)
            if match:
                self.buffer = self.buffer[match.end(0):]
                self.reply_future.set_result((index, match))
                return

    async def get_reply(self, timeout, *reply_templates):
        self.reply_future = ReplyFuture(timeout, reply_templates)
        self.check_msg()
        try:
            return await self.reply_future
        except asyncio.CancelledError:
            raise
