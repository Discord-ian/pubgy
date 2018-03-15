import asyncio
import aiohttp
import weakref
import logging
from .struct import Match, Player, Shard
from .constants import SHARD_LIST, DEFAULT_SHARD, BASE_URL, DEBUG_URL, SORTS
# include a dot because its in the same directory,
# specific import also useful
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
        self.locks = weakref.WeakValueDictionary({})

  
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

    async def match_info(self, match_id, shard):
        if match_id is None:
            route = Route("matches", shard)
        else:
            route = Route("matches/{}".format(match_id), shard)
        resp = await self.request(route)
        print(resp)
        return Match(id=match_id, tel=None, partis=None, shard=shard)

    async def user_matches(self, username, *shard, filter = None):
        filt = filter
        if filt is None:
            filt = self.sorts["ascending"]
        elif filt in self.sorts:
            filt = self.sorts[filt]
        else:
            filt = self.sorts["ascending"]
            log.error("You put in the wrong value for user_matches(filter)")
        route = Route("matches?filter[playerIds]={}&sort={}".format(username, filt))
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

