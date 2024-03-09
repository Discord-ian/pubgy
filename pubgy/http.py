"""
Copyright (c) 2018-2021 Discordian

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import asyncio
import aiohttp
from aiohttp import web
import weakref
import time  # ????
import json
import logging
import warnings
from .exceptions import *
from .objects.player import Player
from .objects.match import Match
from .objects.telemetry import Telemetry
from .objects.stats import Stats
from .constants import *
from .seasons import SEASONS


log = logging.getLogger(__name__)


class Route:
    base = BASE_URL

    def __init__(self, method, shard=None, dataId="", url=None, platform=None):
        """
        Generate Route object with Route.url and Route.tool

        :param method: The intended endpoint (e.g. 'leaderboards', 'players')
        :type method: str
        :param shard: The shard the data is on
        :type shard: str
        :param dataId: A unique ID related to the data (e.g. match id, player id)
        :type dataId: str
        :param url: Not always used, used when special formatting is not needed
        :type url: str
        :param platform: The platform-region the data is on, rarely used (except in leaderboards)
        :type platform: str
        """
        self._method = method
        self._url = url
        self.shard = shard
        self.id = dataId
        self.platform = platform
        if self._method is None:
            self.url = url
        elif "?filter[" in self._method:
            self.url = self.base + self.shard + "/" + self._method + self.id
        elif self._method == "telemetry":
            self.url = url
        elif self._method == "stats":
            self.url = (
                self.base + self.shard + "/players/" + self.id + "/seasons/" + self._url
            )
        elif self._method == "leaderboards":
            self.url = (
                self.base + self.platform + "/leaderboards/" + self.id + "/" + self._url
            )
        elif self._method == "test":
            self.url = self._url
        else:
            self.url = self.base + self.shard + "/" + self._method + "/" + self.id

    @property
    def tool(self):
        return "{0.shard}:{0.method}:{0.id}: {0.url}".format(self)

    @property
    def method(self):
        return self._method


class Query:

    def __init__(self, loop, auth, shard=DEFAULT_SHARD):
        self.loop = asyncio.get_event_loop()
        self.shardID = shard
        self.shards = SHARD_LIST
        self.headers = {"Authorization": auth, "Accept": "application/vnd.api+json"}
        self.headers_gzip = {
            "Authorization": auth,
            "Accept": "application/json",
            "Accept-Encoding": "gzip",
        }
        self.locks = weakref.WeakValueDictionary()

    @property
    def shard(self):
        return self.shardID

    @property
    def isquery(self):
        return True

    def _check_shard(self, shard):
        if isinstance(shard, list) and len(shard) > 1:
            shardList = []
            for item in shard:
                if item not in self.shards:
                    warnings.warn(
                        "Passed shard {}, which is invalid.".format(shard), InvalidShard
                    )
                    shard = self.shardID
                else:
                    shardList.append(shard)
        elif isinstance(shard, list):
            shard = shard[0]
        if shard is None:
            shard = self.shardID
        if shard not in self.shards:
            # TODO: ensure all valid shards are implemented before uncommenting
            warnings.warn(
                "Passed shard {}, which is invalid.".format(shard), InvalidShard
            )
            shard = self.shardID
        return shard

    def _find_matches(self, data):
        id_list = []
        for item in data["relationships"]["matches"]["data"]:
            id_list.append(
                Match(matchID=item["id"], participants=None, shard=None, winners=None)
            )
        return id_list

    async def request(self, route, headers=None):
        tool = route.tool  # debug purposes only, contains information about the request
        url = route.url
        if headers is None:
            headers = self.headers_gzip  # add gzip disable just in case
        lock = self.locks.get(key=tool)
        if lock is None:
            lock = asyncio.Lock()
            if tool is not None:
                self.locks[tool] = lock
        errorc = (
            0  # error counting to avoid constantly requesting if somethings gone wrong
        )
        async with lock:
            async with aiohttp.ClientSession(loop=self.loop) as session:
                for tries in range(2):
                    r = await session.request(method="GET", url=url, headers=headers)
                    log.debug(msg="Requesting {}".format(tool))
                    if r.status == 200:
                        log.debug(msg="Request {} returned: 200".format(tool))
                        return json.loads(await r.text())
                    elif r.status == 401:
                        raise InvalidAPIKey("Your API key is invalid")
                    elif r.status == 404:
                        raise aiohttp.web.HTTPNotFound()  # TODO: error or exception?
                    elif r.status == 429:
                        log.error(
                            "Too many requests.  Wait before making additional requests"
                        )
                        return 429  # TODO: ratelimit management
                    else:
                        errors = await r.json()
                        # TODO: handle_error(errors, tries)
                        try:
                            log.error(
                                "{} | Some other error has occurred. {} - {}".format(
                                    r.status,
                                    errors["errors"][0]["title"],
                                    errors["errors"][0].get("detail"),
                                )
                            )
                        except KeyError:
                            log.error(
                                "KeyError, please report this as an issue on GitHub and attach the following "
                                "info:\nStatus {}\nResp {}\n".format(r.status, errors)
                            )
                        break
                if errorc == 2:
                    r = await session.request(method="GET", url=DEBUG_URL)
                    if r.status != 200:
                        log.error("The API is down or unreachable.")
                await session.close()
                await r.release()

    async def sample_info(self, length=1, shard=None):
        shard = self._check_shard(shard)
        route = Route(SAMPLE_ROUTE, shard)
        resp = await self.request(route)
        _list = await self.check_type(resp)
        return await self.match_info(id=_list[:length], shard=shard)

    async def get_player(self, shard=None, name=None, id=None):
        shard = self._check_shard(shard)
        if name is not None:
            route = Route(PLAYERNAME_ROUTE, shard, name)
            try:
                resp = await self.request(route)
            except aiohttp.web.HTTPNotFound:
                logging.warning("Invalid Player Name")
                return None
            data = resp["data"][0]
            id_list = []
            # for item in data["relationships"]["matches"]["data"]:
            #    id_list.append(Match(id=item["id"], participants=None, shard=None, winners=None))
            return Player(
                name=data["attributes"]["name"],
                pId=data["id"],
                stats=data["attributes"]["stats"],
                shard=data["attributes"]["shardId"],
                uid=None,
            )  # #matchlist=self._find_matches(data))
        else:
            if "," in id:
                route = Route(PLAYERIDLIST, shard, id)
                resp = await self.request(route)
                data = resp["data"]
                ply_list = []
                for player in data:
                    ply_list.append(
                        Player(
                            name=player["attributes"]["name"],
                            pId=player["id"],
                            stats=player["attributes"]["stats"],
                            shard=player["attributes"]["shardId"],
                            uid=None,
                            matchlist=None,
                        )
                    )
                return ply_list
            route = Route(PLAYERID_ROUTE, shard, id)
            resp = await self.request(route)
            data = resp["data"]
            return Player(
                name=data["attributes"]["name"],
                pId=data["id"],
                stats=data["attributes"]["stats"],
                shard=data["attributes"]["shardId"],
                uid=None,
                matchlist=self._find_matches(data),
            )

    async def match_info(self, shard=None, id=None, sorts=None):
        """
        Gets match info from the API.
        This function is a coroutine.

        :param shard: shard to get data from. Defaults to Query.shard
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
            route = Route(path, shard, dataId=id)
        elif isinstance(id, list):
            log.info("Requesting {} matches...".format(len(id)))
            matches = []
            i = 0
            for match in id:
                if i != 50:
                    i += 1
                    route = Route(path, shard, dataId=match)
                    resp = await self.request(route)
                    matches.append(await self.check_type(resp))
            return matches
        else:
            route = Route(path, shard)
        resp = await self.request(route)
        return await self.check_type(resp)

    async def check_type(self, resp):
        """
        Checks if data recieved was a sample object, or something else.

        :param resp: Response from self.request()
        :type resp: Dict or json
        """
        resp = dict(resp)
        tel = ""
        if resp["data"]["type"] == "sample":
            shard = resp["data"]["attributes"]["shardId"]
            match_list = []
            for match in resp["data"]["relationships"]["matches"]["data"]:
                match_list.append(match["id"])
            return match_list
        else:
            return self.parse_resp(resp)

    async def solve_telemetry(self, tel_url):
        route = Route(method="telemetry", url=tel_url)
        resp = await self.request(route)
        return resp

    def parse_resp(self, resp):
        resp = dict(resp)
        ply_list = []
        winners = []
        shard_id = []
        for_matches = {}
        tel_url = ""
        for item in resp["included"]:
            if item["type"] == "participant":
                c_shard = item["attributes"]["shardId"]
                if c_shard not in for_matches:
                    for_matches[c_shard] = []
                for_matches[c_shard].append(item["attributes"]["stats"]["playerId"])
                if item["attributes"]["shardId"] not in shard_id:
                    shard_id.append(item["attributes"]["shardId"])
                ply_list.append(
                    Player(
                        name=item["attributes"]["stats"]["name"],
                        pId=item["id"],
                        stats=item["attributes"]["stats"],
                        shard=item["attributes"]["shardId"],
                        uid=item["attributes"]["stats"]["playerId"],
                    )
                )
                if item["attributes"]["stats"]["winPlace"] == 1:
                    winners.append(
                        Player(
                            name=item["attributes"]["stats"]["name"],
                            pId=item["id"],
                            stats=item["attributes"]["stats"],
                            shard=item["attributes"]["shardId"],
                            uid=item["attributes"]["stats"]["playerId"],
                        )
                    )
            elif item["type"] == "asset":
                if item["attributes"]["name"] == "telemetry":
                    tel_url = item["attributes"]["URL"]
        return Match(
            participants=ply_list,
            matchID=resp["data"]["id"],
            shard=shard_id,
            winners=winners,
            telemetry=tel_url,
            map=resp["data"]["attributes"]["mapName"],
            matchType=resp["data"]["attributes"]["matchType"],
            gameMode=resp["data"]["attributes"]["gameMode"],
        )

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
                    formatted += item + ","
                resp = await self.get_player(id=formatted[:-1], shard=shard)
                finallist.append(resp)
        return finallist

    async def get_stats(self, id, shard, season):
        shard = self._check_shard(shard)
        url = Route(url=STATS[season], shard=shard, dataId=id, method="stats")
        resp = await self.request(url)
        return Stats(resp["data"]["attributes"]["gameModeStats"]["solo"])

    # def parse_leaderboard(self, resp):

    """
    Leaderboards are treated very weirdly within PUBG due to changes over time with cross-platform play and what not.
    This is a basic explanation of why I have done what I have done, and some advice if you want to change this code.
    Below is commented out code that helped me reach this conclusion
    
    """

    def _is_platform_shard(self, shard):
        if shard in PLATFORM_REGION:
            return True
        return False

    async def test_seasons_leaderboards(
        self,
    ):  # leaving this here just in case it becomes useful again (hope not)
        shard_list = SHARD_LIST
        platform_region_list = [
            "pc-na",
            "psn-na",
            "xbox-na",
        ]
        season_list = {"PC": [], "XBOX": [], "PS4": [], "Stadia": []}
        platform_to_shard = {
            "PC": ["steam", "pc-na"],
            "XBOX": ["xbox", "xbox-na"],
            "PS4": ["psn", "psn-na"],
        }
        evaluated = {
            "PC": {"platform": [], "platform-region": []},
            "XBOX": {"platform": [], "platform-region": []},
            "PS4": {"platform": [], "platform-region": []},
            "Stadia": {"platform": [], "platform-region": []},
        }
        for (
            platform_name
        ) in SEASONS:  # gets all season ids and puts them in a list for each platform
            if platform_name == "Stadia":
                break
            for season_title in SEASONS[platform_name]:
                season_list[platform_name].append(season_title["id"])
        for platform_name in SEASONS:  # pc xbox ps4 stadia
            for season_id in season_list[
                platform_name
            ]:  # division.bro.official.2018-02
                for shard_name in platform_to_shard[
                    platform_name
                ]:  # platform_name = PC/PS4/XBOX
                    try:
                        async with aiohttp.ClientSession(
                            headers=self.headers
                        ) as session:  # https://api.pugb.com/shards/
                            url = "{}{}/leaderboards/{}/solo".format(
                                BASE_URL, shard_name, season_id
                            )
                            logging.debug("Request @ " + url)
                            r = await session.request(method="GET", url=url)
                            try:
                                temp = await r.json()
                                r_length = len(
                                    temp["data"]["relationships"]["players"]["data"]
                                )
                                logging.info(
                                    "Length: {} -- Status: {}".format(
                                        r_length, r.status
                                    )
                                )
                            except Exception as e:
                                logging.error(e)
                            if r.status == 404:
                                break
                            if r_length != 0:
                                if self._is_platform_shard(shard_name):
                                    evaluated[platform_name]["platform-region"].append(
                                        season_id
                                    )
                                else:
                                    evaluated[platform_name]["platform"].append(
                                        season_id
                                    )
                        await asyncio.sleep(7)  # avoid spamming API
                    except Exception as e:
                        logging.error(e)
        print(evaluated)

    """Output of function above: 
    {'PC': {'platform': ['division.bro.official.pc-2018-01', 
    'division.bro.official.pc-2018-02', 'division.bro.official.pc-2018-03', 'division.bro.official.pc-2018-04', 
    'division.bro.official.pc-2018-05', 'division.bro.official.pc-2018-06', 'division.bro.official.pc-2018-07'], 
    'platform-region': ['division.bro.official.pc-2018-01', 'division.bro.official.pc-2018-02', 
    'division.bro.official.pc-2018-03', 'division.bro.official.pc-2018-04', 'division.bro.official.pc-2018-05', 
    'division.bro.official.pc-2018-06']}, 'XBOX': {'platform': ['division.bro.official.xbox-01', 
    'division.bro.official.xbox-02', 'division.bro.official.console-03', 'division.bro.official.console-04', 
    'division.bro.official.console-05', 'division.bro.official.console-06', 'division.bro.official.console-07', 
    'division.bro.official.console-10'], 'platform-region': ['division.bro.official.xbox-01', 
    'division.bro.official.xbox-02', 'division.bro.official.console-03', 'division.bro.official.console-04', 
    'division.bro.official.console-05', 'division.bro.official.console-06', 'division.bro.official.console-09', 
    'division.bro.official.console-10']}, 'PS4': {'platform': ['division.bro.official.2018-09', 
    'division.bro.official.playstation-01', 'division.bro.official.playstation-02', 
    'division.bro.official.console-03', 'division.bro.official.console-04', 'division.bro.official.console-05', 
    'division.bro.official.console-06', 'division.bro.official.console-07', 'division.bro.official.console-10'], 
    'platform-region': ['division.bro.official.playstation-01', 'division.bro.official.playstation-02', 
    'division.bro.official.console-03', 'division.bro.official.console-04', 'division.bro.official.console-05', 
    'division.bro.official.console-06', 'division.bro.official.console-09', 'division.bro.official.console-10']}, 
    'Stadia': {'platform': [], 'platform-region': []}} 
    """

    async def leaderboard_info(self, platform, season, gamemode):
        # platform = self._check_platform(platform)
        url = Route(
            url=gamemode, dataId=season, method=LEADERBOARD_ROUTE, platform=platform
        )
        resp = await self.request(url)
        with open("../debug/leaderboardresp.json", "w+") as out:
            json.dump(resp, out)
        # return parse_leaderboard(resp)

    def _generate_query_string(self, keys):
        """
        Generates the string to give to Route.

        :param keys: Filter object
        :type filter: A filter object
        :returns: A query param string starting in ? and separated by &
        """
        if len(keys) == 0:  # todo: what is this
            return ""
        result = "?"
        if filter.sorts is None:

            if filter.length is not None:
                result = "{}page[limit]={}&".format(result, filter.length)
            if filter.offset is not None:
                result = "{}page[offset]={}&".format(result, filter.offset)
            # need to add more filters to distinguish between players, etc
        for k, v in filter.sorts:
            result = "{}{}={}&".format(
                result, k, v
            )  # append to the current result a key value pair
        return result[:-1]  # trim the result to remove trailing &
