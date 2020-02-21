import asyncio
import aiohttp
import weakref
import time
import logging
from .struct import *
import json
from .constants import *
log = logging.getLogger(__name__)


class Route:
    base = BASE_URL

    def __init__(self, method, shard, id=""):
        self.method = method
        self.shard = shard
        self.id = id
        if "?filter[" in self.method:
            self.url = self.base + self.shard + "/" + self.method + self.id
        else:
            self.url = self.base + self.shard + "/" + self.method + "/" + self.id

    @property
    def tool(self):
        return '{0.shard}:{0.method}:{0.id}: {0.url}'.format(self)


class Query:

    def __init__(self, loop, auth, shard=DEFAULT_SHARD):
        self.loop = loop
        self.shardID = shard
        self.shards = SHARD_LIST
        #self.sorts = SORTS
        self.headers = {
            "Authorization": auth,
            "Accept": "application/vnd.api+json"
        }
        #self.session = aiohttp.ClientSession(loop=self.loop)
        self.locks = weakref.WeakValueDictionary()

    @property
    def shard(self):
        return self.shardID

    def _check_shard(self, shard):
        if shard not in self.shards:
            log.warn("Invalid shard passed. Defaulting to {}".format(self.shardID))
            return self.shardID
        else:
            return shard

    def _find_matches(self, data):
        id_list = []
        for item in data["relationships"]["matches"]["data"]:
            id_list.append(Match(id=item["id"], participants=None, shard=None, winners=None))
        return id_list

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
            async with aiohttp.ClientSession(loop=self.loop) as session:
                for tries in range(2):
                    r = await session.request(method='GET', url=url, headers=self.headers)
                    log.debug(msg="Requesting {}".format(tool))
                    if r.status == 200:
                        log.debug(msg="Request {} returned: 200".format(tool))
                        return await r.json()
                    elif r.status == 401:
                        log.warn("Your API key is invalid or there was an internal server error.")
                        return None
                    elif r.status == 429:
                        log.error("Too many requests.")
                        return 429
                    else:
                        errors = await r.json()
                        log.error("{} | Some other error has occured. Investigating. . . | {} - {}".format(r.status, errors['errors'][0]['title'], errors['errors'][0]['detail']))
                        break
                if errorc == 2:
                    r = await session.request(method='GET', url=DEBUG_URL)
                    if r.status != 200:
                        log.error("The API is down or unreachable.")
                await session.close()
                await r.release()

    async def sample_info(self, length=1, shard=None):
        """
        Gets
        :param shard:
        :return:
        """
        shard = self._check_shard(shard)
        route = Route(SAMPLE_ROUTE, shard)
        resp = await self.request(route)
        list = await self.check_type(resp)
        return await self.match_info(id=list[length])

    async def get_player(self, shard=None, name=None, id=None):
        shard = self._check_shard(shard)
        if name is not None:
            route = Route(PLAYERNAME_ROUTE, shard, name)
            resp = await self.request(route)
            data = resp["data"][0]
            id_list = []
            for item in data["relationships"]["matches"]["data"]:
                id_list.append(Match(id=item["id"], participants=None, shard=None, winners=None))
            return Player(name=data["attributes"]["name"], id=data["id"], stats=data["attributes"]["stats"], shard=data["attributes"]["shardId"], uid=None, matchlist=self._find_matches(data))
        else:
            if "," in id:
                route = Route(PLAYERIDLIST, shard, id)
                resp = await self.request(route)
                data = resp["data"]
                ply_list = []
                for player in data:
                    ply_list.append(Player(name=player["attributes"]["name"], id=player["id"], stats=player["attributes"]["stats"], shard=player["attributes"]["shardId"], uid=None, matchlist=None))
                return ply_list
            else:
                route = Route(PLAYERID_ROUTE, shard, id)
            resp = await self.request(route)
            data = resp["data"]
            return Player(name=data["attributes"]["name"], id=data["id"], stats=data["attributes"]["stats"], shard=data["attributes"]["shardId"], uid=None, matchlist=self._find_matches(data))

    async def match_info(self, shard=None, id=None, sorts=None):
        """
        Gets match info from the API.
        This function is a coroutine.

        :param shard: Shard to get data from. Defaults to Query.shard
        :param filter: A Filter object to determine what results you want back
        :type filter: a Filter object made with pubgy.utils.filter
        :type id: Match ID. If none is provided, it will return 5 match objects.
        :param sorts: A more direct method of interacting with the api.
        :type sorts: A dict filled with sorting methods
        :returns: The amount of match objects requested.
        """
        path = MATCHES_ROUTE
        shard = self._check_shard(shard)
        query_params = {}
        if id is not None and not isinstance(id, list):
            route = Route(path, shard, id=id)
        elif isinstance(id, list):
            log.info("Requesting {} matches...".format(len(id)))
            matches = []
            i = 0
            for match in id:
                if i != 50:
                    i += 1
                    route = Route(path, shard, id=match)
                    resp = await self.request(route)
                    matches.append(await self.check_type(resp))
            return matches
        else:
            route = Route(path, shard)
        resp = await self.request(route)
        #with open("match.json", "w") as file:
        #    json.dump(resp, file)         #obtain a sample match file so i can format this garbage
        return await self.check_type(resp)

    async def check_type(self, resp):
        """
        Checks if data recieved was a sample object, or something else.
        This function is a coroutine.
        
        :param resp: Response from self.request()
        :type resp: Dict or json
        """
        match_list = []
        resp = dict(resp)
        tel = ""
        if resp["data"]["type"] == "sample":
            shard = resp["data"]["attributes"]["shardId"]
            match_list = []
            for match in resp["data"]["relationships"]["matches"]["data"]:
                match_list.append(match["id"])
            return match_list
        else:
            return await self.parse_resp(resp)


    async def parse_resp(self, resp):
        resp = dict(resp)
        ply_list = []
        winners = []
        shardId = []
        for_matches = {}
        for item in resp["included"]:
            if item["type"] == "participant":
                cshard = item["attributes"]["shardId"]
                if cshard not in for_matches:
                    for_matches[cshard] = []
                for_matches[cshard].append(item["attributes"]["stats"]["playerId"])
        #await self._get_player_matches(for_matches)
                if item["attributes"]["shardId"] not in shardId:
                    shardId.append(item["attributes"]["shardId"])
                ply_list.append(Player(name=item["attributes"]["stats"]["name"],id=item["id"],stats=item["attributes"]["stats"],shard=item["attributes"]["shardId"],uid=item["attributes"]["stats"]["playerId"]))
                if item["attributes"]["stats"]["winPlace"] == 1:
                    winners.append(Player(name=item["attributes"]["stats"]["name"],id=item["id"],stats=item["attributes"]["stats"],shard=item["attributes"]["shardId"],uid=item["attributes"]["stats"]["playerId"]))
        toReturn = Match(participants=ply_list,id=resp["data"]["id"],shard=shardId,winners=winners)
        return toReturn

    async def _get_player_matches(self, idlist):
        finallist = []
        tosend = {}
        for item in idlist:
            if item not in tosend:
                tosend[item] = []
            while len(idlist[item]) != 0:
                tosend[item].append(idlist[item][:10])
                for topop in idlist[item][:10]:
                    idlist[item].remove(topop)
        for shard in tosend:
            for request in tosend[shard]:
                formatted = ""
                for item in request:
                    formatted += (item + ",")
                resp = await self.get_player(id=formatted[:-1], shard=shard)
                finallist.append(resp)
        return finallist





    def _generate_query_string(self, filter):
        """
        Generates the string to give to Route.

        :param keys: Filter object
        :type filter: A filter object
        :returns: A query param string starting in ? and separated by &
        """
        if len(keys) == 0:
            return ""
        result = "?"
        if filter.sorts is None:

            if filter.length is not None:
                result = "{}page[limit]={}&".format(result, filter.length)
            if filter.offset is not None:
                result = "{}page[offset]={}&".format(result, filter.offset)
            # need to add more filters to distinguish between players, etc
        for k, v in filter.sorts:
            result = "{}{}={}&".format(result, k, v) # append to the current result a key value pair
        return result[:-1]  # trim the result to remove trailing &

    # maintain pep8
    async def close(self):
        await self.session.close()
