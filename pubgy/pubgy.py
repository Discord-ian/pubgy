import asyncio
from .http import Query


class Pubgy:

    def __init__(self, auth_token):
        self.auth = auth_token
        self.loop = asyncio.get_event_loop()
        self.web = Query(self.loop, self.auth)

    async def get_match_info(self, match_id, shard):
        return await self.web.match_info(match_id, shard)
