import asyncio
import aiohttp
import weakref
import logging
from .struct import Match, Player, Shard
from .constants import *
# include a dot because its in the same directory,
log = logging.getLogger(__name__)


class Route:
    base = BASE_URL

    def __init__(self, method, shard):
        self.method = method
        self.shard = shard
        # got rid of self.shard and shard from init
        self.url = self.base + self.method  # no shard support
        # self.url = self.base + self.shard + / + self.method

    @property
    def tool(self):
        return '{0.shard}:{0.method} : {0.url}'.format(self)


class Query:

    def __init__(self, loop, auth, shard=DEFAULT_SHARD):
        self.loop = loop
        self.shardID = shard
        self.shards = SHARD_LIST
        self.sorts = SORTS
        self.headers = {
            "Authorization": auth,
            "Accept": "application/json"
        }
        self.session = aiohttp.ClientSession(loop=self.loop)
        self.locks = weakref.WeakValueDictionary()
        # needs no arguments to init.

    @property
    def shard(self):
        return self.shardID

    async def request(self, route):
        tool = route.tool
        url = route.url
        lock = self.locks.get(key=tool)
        if lock is None:
            lock = asyncio.Lock(loop=self.loop)
            if tool is not None:
                self.locks[tool] = lock
        errorc = 0
        async with lock:
            for tries in range(2):
                r = await self.session.request(method='GET', url=url, headers=self.headers)
                log.debug(msg="Requesting {}".format(tool))
                try:
                    if r.status == 200:
                        log.debug(msg="Request {} returned: 200".format(tool))
                        return r.json()
                    elif r.status == 429:
                        log.error("Too many requests.")
                        return 429
                    else:
                        log.error("Some other error has occured. Investigating. . . ")
                        errorc += 1
                finally:
                    await r.release()
            if errorc == 2:
                r = await self.session.request(method='GET', url=DEBUG_URL)
                if r.status == 401:
                    log.error("Your API key is invalid or there was an internal server error.")
                    self.session.close()
                elif r.status != 200:
                    log.error("The API is down or unreachable.")
                    self.session.close()

    async def match_info(self,shard=None, match_id=None, page_length=None, offset=0):
        """

        :param shard: Shard to get data from. Defaults to Query.shard
        :param match_id: Match ID. Defaults to None and gets matches according to filters.
        :param page_length: No idea what this does
        :param offset: Tells how far down for it to start retrieving data.
        :returns: The amount of match objects requested.
        """
        # remove spaces to maintain pep :P
        path = MATCHES_ROUTE
        query_params = {}
        if match_id is not None:
            path = "{}/{}".format(path, match_id)
        if page_length is not None:
            query_params.update({'page[length]': page_length, 'page[offset]': offset})
        path = path + self._generate_query_string(query_params)
        route = Route(path, shard)
        resp = await self.request(route)
        print(resp)
        return Match(id=match_id, tel=None, partis=None, shard=shard)

    async def user_matches(self, username, *shard, filts=None):
        filt = filts
        # change because filter is an internal arg
        query_params = {'filter[playerIds]': username}
        if filt is None:
            filt = self.sorts["ascending"]
        elif filt in self.sorts:
            filt = self.sorts[filt]
        else:
            filt = self.sorts["ascending"]
            log.error("You put in the wrong value for user_matches(filter)")
            return 400
        query_params.update({'sort': filt})
        route = Route(MATCHES_ROUTE + self._generate_query_string(query_params), shard)
        resp = await self.request(route)
        # for key =
        # need to iterate over the match objects.
        # same thing with match_info

    async def user_info(self, username, shard):
        route = Route("", shard)  # route not determined

    def _generate_query_string(self, keys):
        """
        :param keys: dictionary containing names of query params and values
        :type keys: dict
        :returns: A query param string starting in ? and separated by &
        """
        if len(keys) == 0:
            return ""
        result = ""
        for k, v in keys.items():
            result = "?{}={}&".format(k, v)
            # do we need an & at the end? also, should we check since we don't need a ? unless its filter #1
        return result[:-1]

    # maintain pep8
    async def close(self):
        await self.session.close()

