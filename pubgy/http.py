import asyncio
import aiohttp
import weakref
import logging

log = logging.getLogger(__name__)


class Route:
    base = "https://api.playbattlegrounds.com/shards/"

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
        self.shards = ["xbox-as", "xbox-eu", "xbox-na", "xbox-oc",
                       "pc-krjp", "pc-na", "pc-eu", "pc-oc", "pc-kakao",
                       "pc-sea", "pc-sa", "pc-as"]
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

    @asyncio.coroutine
    async def close(self):
        await self.session.close()






