import asyncio
import aiohttp
import weakref
import logging
from .struct import Match, Player
import constants
log = logging.getLogger(__name__)


class Route:
    base = BASE_URL

    def __init__(self, method, shard):
        self.method = method
        self.shard = shard
        self.url = self.base + self.shard + "/" + self.method

    @property
    def tool(self):
        return '{0.shard}:{0.method}:{0.url'.format(self)


class Query:

    def __init__(self, loop, auth):
        self.loop = loop
        self.shards = SHARD_LIST
        self.headers = {
            "Authorization": auth,
            "Accept": "application/json"
        }
        self.session = aiohttp.ClientSession(loop=self.loop)
        self.locks = weakref.WeakValueDictionary

    async def request(self, route):
        tool = route.tool
        url = route.url
        lock = self.locks.get(tool, default=None)
        if lock is None:
            lock = asyncio.Lock(loop=self.loop)
            if tool is not None:
                self.locks[tool] = lock

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
                finally:
                    await r.release()

    async def match_info(self, match_id, shard):
        route = Route("matches/{}".format(match_id), shard)
        resp = await self.request(route)
        resp = resp.json()
        return Match(id=match_id, tel=resp["data"][0]["asset"])

    async def user_matches(self, username, shard, *parse : True):
        route = Route("matches?filter[playerIds]={}&sort=-createdAt".format(username), shard)
        resp = await self.request(route)
        resp = resp.json()
        rev = {}
        count = 0
        for item in resp['data']:
            name = "Match{}".format(count)
            rev[name] = resp['data'][count]
            count += 1
        if parse:
            return self.parse_match_data(rev)

    async def user_info(self, username, shard):
        route = Route("") #route not determined

    async def parse_match_data(self, match):
        count = 0
        for item in range(4):





    @asyncio.coroutine
    async def close(self):
        await self.session.close()






