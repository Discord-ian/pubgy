import asyncio
from .http import Query


class Pubgy:

    def __init__(self, auth_token):
        """
        :param auth_token: The API Authentication token
        :type auth_token: str
        :returns: A Pubgy object to do requests from.
        """
        self.auth = auth_token
        self.aloop = asyncio.get_event_loop()
        self.web = Query(self.aloop, self.auth)

    async def print_json(self, match_id=None):
        return await self.web.match_info()

    def close(self):
        self.web.close()
        self.aloop.close()

    async def match(self, match_id=None, shard=None, amount=None, offset=0, filter=None):
        """
        This function is a coroutine.
        Gets specific match info depending on the parameters supplied.

        :param match_id: Defaults to None.
        :type match_id: str or None
        :type shard: str or None
        :param shard: Defaults to Query.shard
        :type amount: int
        :param amount: Defaults to 5, only returns the amount of match objects equal to length
        :type offset: int
        :param offset: Defaults to 0, where to start parsing the stats from.
        :returns: A populated Match object.
        """
        if shard is None:
            shard = self.web.shard
        return await self.web.match_info(match_id=match_id, shard=shard, page_length=length, offset=offset)

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
