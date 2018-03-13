import asyncio
from .http import Query


class Pubgy:

    def __init__(self, auth_token):
        self.auth = auth_token
        self.aloop = asyncio.get_event_loop()
        self.web = Query(self.loop, self.auth)

    async def get_match_info(self, *, match_id=None, shard=None):
        if shard is None:
            shard = self.web.shard
        return await self.web.match_info(match_id=match_id, shard=shard)

    @property
    def shard(self):
        return self.web.shard

    @property
    def loop(self):
        return self.aloop


