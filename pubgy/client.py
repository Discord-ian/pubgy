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

    def close(self):
        """
        Closes both the webloop and the asyncio loop. Run before ending your own clients loop.
        """
        self.web.close()
        self.aloop.close()

    async def match(self, shard=None, sorts=None, filter=None):
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
        return await self.web.match_info(shard=shard, sorts=sorts, filter=filters)

    async def solve(self, telemetry):
        """
        This function is a coroutine.
        Puts a Telemetry object into a useful set of data.

        :param telemetry: A telemetry object that has just been recieved from a match.
        :type telemetry: A Telemetry object with only telemetry.url filled.
        """

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
