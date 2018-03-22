import asyncio
import aiohttp
import weakref
import logging
from .struct import Match, Player, Team
from .constants import *
# include a dot because its in the same directory,
log = logging.getLogger(__name__)


class Route:
    base = BASE_URL

    def __init__(self, method, shard):
        self.method = method
        self.shard = shard
        # got rid of self.shard and shard from init
        self.url = self.base + self.shard + "/" + self.method  # no shard support
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
            "Accept": "application/vnd.api+json"
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
                        return await r.json()
                    elif r.status == 401:
                        log.error("Your API key is invalid or there was an internal server error.")
                        self.session.close()
                        return None
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
                if r.status != 200:
                    log.error("The API is down or unreachable.")
                    self.session.close()

    async def match_info(self, shard=None, filter=Filter(sort="-createdAt", length=5, offset=0)):
        """
        Gets match info from the API.
        This function is a coroutine.

        :param shard: Shard to get data from. Defaults to Query.shard
        :param filter: A Filter object to determine what results you want back
        :type filter: a Filter object made with pubgy.utils.filter
        :returns: The amount of match objects requested.
        """
        # remove spaces to maintain pep :P
        path = MATCHES_ROUTE
        if shard is None:
            shard = self.shard
        query_params = {}
        if filter.matchid is not None:
            path = "{}/{}".format(path, filter.matchid)
        if page_length is not None:
           query_params.update({'page[limit]': filter.length, 'page[offset]': filter.offset})
           path = path + self._generate_query_string(query_params)
        print(path)
        route = Route(path, shard)
        resp = await self.request(route)
        tel = await self.get_telemetry(resp)
        return Match(id=resp['data'][0]['id'], partis=tel['partis'], shard=resp['data'][0]['attributes']['shardId'], tel=tel['telemetry'])

    async def user_match(self, filter, shard=None):
        query_params = {'filter[playerIds]': filter.userid}
        if shard is None:
            shard = self.shard
        query_params.update({'sort': filter.sort})
        route = Route(MATCHES_ROUTE + self._generate_query_string(query_params), shard)
        resp = await self.request(route)
        respList = []
        tel = await self.get_telemetry(resp)
        for match in resp['data']:
            respList.append(Match(id=match['id'], partis=tel['teams'], shard=match['attributes']['shardId'], tel=tel['telemetry']))
        return respList

    async def user_info(self, username, shard):
        route = Route("", shard)  # route not determined

    async def get_telemetry(self, resp):
        partis = {}
        teams = []
        players = []
        teamList = []
        resp = dict(resp)
        tel = ""
        for key in resp['included']:
            if key['type'] == "participant":
                partis[key['id']] = Player(uid=key['id'], name=key['attributes']['stats']['name'], id=key['attributes']['stats']['playerId'], shard=key['attributes']['shardId'], stats=key['attributes']['stats'])
            elif key['type'] == "asset":
                tel = key['attributes']['URL']
            elif key['type'] == "roster":
                teams.append(key)
            else:
                pass
        for team in teams:
            players = []
            for part in team['relationships']['participants']['data']:
                players.append(partis[part['id']])
            teamList.append(Team(players=players, id=team['id'], data=team))
        return {"partis": partis, "telemetry": tel, "teams": teamList}

    def _generate_query_string(self, filter):
        """
        Generates the string to give to Route.

        :param keys: dictionary containing names of query params and values
        :type keys: dict
        :returns: A query param string starting in ? and separated by &
        """
        if len(keys) == 0:
            return ""
        result = "?"
        for k, v in filter.sorts:
            result = "{}{}={}&".format(result, k, v) # append to the current result a key value pair
        return result[:-1]  # trim the result to remove trailing &

    # maintain pep8
    async def close(self):
        await self.session.close()
