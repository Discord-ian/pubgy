import asyncio
from .http import Query
from .parse import Parser
from .exceptions import InvalidPlayerID
from .objects import Player


class Pubgy:
    """
    Represents the core of PUBGy.
    Start by initializing an instance of it, using ::

        import pubgy
        client = pubgy.Pubgy("your auth token")

    """
    def __init__(self, auth_token, defaultshard=None):
        """
        :param auth_token: The API Authentication token
        :type auth_token: str
        :param defaultshard: A Shard from the list of shards in :class`constants.SHARD_LIST`:
        :returns: A Pubgy object to do requests from.
        """
        self.auth = auth_token
        self.aloop = asyncio.get_event_loop()
        self.web = Query(self.aloop, self.auth)
        self.parse = Parser(self.web)

#    async def close(self):
#        """
#        Closes both the webloop and the asyncio loop. Run before ending your own clients loop.
#        """
#        await self.web.close()
#        await self.aloop.close()

    async def player(self, plyname, shard=None):
        """
        This function is a coroutine.
        Gets a player's stats by using either their player name or account id.

        If given a list of player names/ids, they all must be the same type.
        
        :param plyname: A Players name/ID
        :type plyname: str or list
        :return: :class:`.objects.Player`
        """
        # check if plyname is actually a bot
        if self._checkifbot(plyname):
            return InvalidPlayerID
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

    async def stats(self, player, id=None):
        """

        :param player: A player name
        :type player: str
        :param id: A player id (with account)
        :type: str
        :return: A :class:`.objects.Player` with a filled :class:`.objects.Stats` property.
        """
        #TODO: Add support for just sending this function a player id rather than pubgy.Player
        return await self.web.get_stats(shard=player.shard, id=player.id, season="all")

    async def _generate_telemetry(self, telemetry, match=None):
        """

        :param telemetry:
        :type telemetry: str
        :return:
        """
        return await self.parse.telemetry(telemetry, match=match)

    async def samples(self, shard=None, amount=1):
        """
        This function is a coroutine.
        Gets sample matches from the /samples endpoint

        :type shard: str or None
        :param shard: Defaults to shard passed on client initialization
        :type amount: int
        :param amount: Defaults to 1, only returns the amount of match objects equal to length
        :returns: A populated :class:`.objects.Match` or a list of :class:`.objects.Match` if amount > 1
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
        :returns: :class:`.objects.Match`
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

    def _checkifbot(self, playernames):
        if isinstance(playernames, list):
            for id in playernames:
                if "ai." in id:
                    return True
        else:
            if "ai." in playernames:
                return True
        return False
