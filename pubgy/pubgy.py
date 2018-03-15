import asyncio
from .http import Query


class Pubgy:

    def __init__(self, auth_token):
        self.auth = auth_token
        self.aloop = asyncio.get_event_loop()
        self.web = Query(self.loop, self.auth)

<<<<<<< HEAD
<<<<<<< Updated upstream
    async def get_match_info(self, match_id, shard):
        return await self.web.match_info(match_id, shard)
=======
    async def get_match_info(self, match_id=None, shard=None):
        """

        :param match_id: Defaults to None.
        :type match_id: str or None
        :type shard: str or None
        :param shard: Defaults to Query.shard
        :returns: A populated Match object.
        """
=======
    async def get_match_info(self, *, match_id=None, shard=None):
>>>>>>> 07f7b699239c1683e5ead41ee9577aceb86facf5
        if shard is None:
            shard = self.web.shard
        return await self.web.match_info(match_id=match_id, shard=shard)

    @property
    def shard(self):
<<<<<<< HEAD
        """
        :returns: The Query.shard (str)
        """
=======
>>>>>>> 07f7b699239c1683e5ead41ee9577aceb86facf5
        return self.web.shard

    @property
    def loop(self):
<<<<<<< HEAD
        """
        :returns: The main asyncio loop.
        """
        return self.aloop


>>>>>>> Stashed changes
=======
        return self.aloop


>>>>>>> 07f7b699239c1683e5ead41ee9577aceb86facf5
