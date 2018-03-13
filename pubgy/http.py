import asyncio
import aiohttp
import weakref
import logging
from .struct import Match, Player
from .constants import SHARD_LIST, BASE_URL
# include a dot because its in the same directory,
# specific import also useful
log = logging.getLogger(__name__)


class Route:
    base = BASE_URL

    def __init__(self, method):
        self.method = method
        # got rid of self.shard and shard from init
        self.url = self.base + self.method  # no shard support
        # self.url = self.base + self.shard + / + self.method

    @property
    def tool(self):
        return '{0.method}:{0.url}'.format(self)


class Query:

    def __init__(self, loop, auth):
        self.loop = loop
        self.shards = SHARD_LIST
        self.headers = {
            "Authorization": auth,
            "Accept": "application/json"
        }
        self.session = aiohttp.ClientSession(loop=self.loop)
        self.locks = weakref.WeakValueDictionary({})

    async def request(self, route):
        tool = route.tool
        url = route.url
        lock = self.locks.get(key=tool)
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
                    else:
                        log.error("Something else went wrong?")
                finally:
                    await r.release()

    async def match_info(self, match_id):
        if match_id is None:
            route = Route("matches")
        else:
            route = Route("matches/{}".format(match_id))
        resp = await self.request(route)
        print(resp)
        return Match(id=match_id, tel=None, partis=None)

    async def user_matches(self, username, *parse : True):
        route = Route("matches?filter[playerIds]={}&sort=-createdAt".format(username))
        resp = await self.request(route)
        resp = resp.json()
        rev = {}
        count = 0
       # for item in resp['data']:\

    async def user_info(self, username, shard):
        route = Route("") # route not determined

    # maintain pep8
    async def close(self):
        await self.session.close()

