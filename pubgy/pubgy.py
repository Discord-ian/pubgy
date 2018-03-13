import asyncio
from .http import Query
import logging


class Pubgy:

    def __init__(self, auth_token):
        self.auth = auth_token
        self.aloop = asyncio.get_event_loop()
        self.web = Query(self.loop, self.auth)

    async def get_match_info(self, match_id=None):
        return await self.web.match_info(match_id)

    @property
    def loop(self):
        return self.aloop

    @property
    def log(self):
        return logging.getLogger(__name__)

