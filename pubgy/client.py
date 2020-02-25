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

    async def close(self):
        """
        Closes both the webloop and the asyncio loop. Run before ending your own clients loop.
        """
        await self.web.close()
        await self.aloop.close()

    async def player(self, plyname, shard=None):
        """
        This function is a coroutine.
        Gets a player's stats by using either their player name or account id.

        If given a list of player names/ids, they all must be the same type.
        
        :param plyname: A Players name/ID
        :type plyname: str or list
        :return: A Player object or list of Player objects.
        """
        if isinstance(plyname, list):
            if plyname[0][:8] == "account.":
                return await self.web.get_player(id=plyname, shard=shard)
            else:
                return await self.web.get_player(name=plyname, shard=shard)
        else:
            if plyname[:8] == "account.":
                return await self.web.get_player(id=plyname, shard=shard)
            else:
                return await self.web.get_player(name=plyname, shard=shard)

    async def samples(self, shard=None, amount=1):
        """
        This function is a coroutine.
        Gets sample matches from the /samples endpoint

        :type shard: str or None
        :param shard: Defaults to shard passed on client initialization
        :type amount: int
        :param amount: Defaults to 1, only returns the amount of match objects equal to length
        :returns: A populated Match object or a list of Match objects if amount > 1
        """
        return await self.web.sample_info(shard=shard, length=amount)

    async def matches(self, id, shard=None, sorts=None, filter=None):
        """
        This function is a coroutine.

        Gets specific match info depending on the parameters supplied.

        :param id: Required.
        :type id: str
        :type shard: str or None
        :param shard: Defaults to Query.shard
        :type amount: int
        :param amount: Defaults to 5, only returns the amount of match objects equal to length
        :type offset: int
        :param offset: Defaults to 0, where to start parsing the stats from.
        :returns: A populated Match object.
        """
        return await self.web.match_info(id=id, shard=shard, sorts=sorts)

    async def solve(self, telemetry):
        """
        This function is a coroutine.

        Puts a Telemetry object into a useful set of data.

        :param telemetry: A telemetry object that has just been received from a match.
        :type telemetry: A Telemetry object with only telemetry.url filled.
        """
        return await self.web.solve_telemetry(telemetry)

    @property
    def shard(self):
        """
        Returns the shard the client was initiated with. This is used as the default shard for all commands,
        unless another one is passed

        :returns: str 
        """
        return self.web.shard

    @property
    def loop(self):
        """
        :returns: The main asyncio loop.
        """
        return self.aloop
