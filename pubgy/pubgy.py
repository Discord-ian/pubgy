import asyncio
from .http import Query


class Pubgy:

    def __init__(self, auth_token):
        self.auth = auth_token
        self.aloop = asyncio.get_event_loop()
        self.web = Query(self.loop, self.auth)

        """

        :param match_id: Defaults to None.
        :type match_id: str or None
        :type shard: str or None
        :param shard: Defaults to Query.shard
        :returns: A populated Match object.
        """
    async def get_match_info(self, *, match_id=None, shard=None, page_length=None, page_offset=None):
        if shard is None:
            shard = self.web.shard
        return await self.web.match_info(match_id=match_id, shard=shard, page_length=page_length, offset=page_offset)

    @property
    def shard(self):
        """
        :returns: The Query.shard (str)
        """
        return self.web.shard

    @property
    def loop(self):
        """
        :returns: The main asyncio loop.
        """
        return self.aloop