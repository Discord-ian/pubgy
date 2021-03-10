from pubgy.constants import *


class Match:
    """
    A Match object
    Returned whenever :func:`pubgy.client.matches` is called.
    """

    def __init__(self, id, participants, shard, winners, telemetry, map, matchType=None, gameMode=None):
        # TODO: matchType != gameMode
        """
        :param id: The match id
        :type id: str
        :param participants:  A list of :class:`objects.Player`
        :type participants: list
        :param shard: Which shard did the match occur on
        :type shard: str
        :param winners: A list of :class:`objects.Player`
        :type winners: list
        :param telemetry: Telemetry URL
        :type telemetry: str
        :param map: Which map did the match occur on
        :type map: str
        :param matchType: What gamemode type was the match
        :type matchType: str
        :returns: A built Match object
        """
        self.matchID = id
        self.participants = participants
        self.shardId = shard
        self.tel = telemetry
        if matchType in MATCH_TYPES:
            self.matchType = matchType
        else:
            self.matchType = "Unknown Match Type"
        self.winner = winners
        self._map = TEL_REF[map]
        self.gameMode = gameMode
        # make a way to make a list of the Player class with everyone who was in the game.

    @property
    def id(self):
        """
        :return: A Match ID (str)
        """
        return self.matchID

    @property
    def map(self):
        """
        :return: Which map the game occurred on (str)
        """
        return self._map

    @property
    def players(self):
        """
        :return: A list of :class:`objects.Player`
        """
        return self.participants

    @property
    def winners(self):
        """
        :return: A list of :class:`objects.Player` who won
        """
        return self.winner

    @property
    def shard(self):
        """
        :return: The shard the match occurred on (str)
        """  # TODO: this will always be a list (and will have to because of console cross platform play) figure something out.
        return self.shardId

    @property
    def telemetry(self):
        """
        :return: The telemetry url (str)
        """
        return self.tel

    @property
    def type(self):
        return self.matchType

    @property
    def gamemode(self):
        return self.gameMode


class Player:

    def __init__(self, name, id, uid, stats, shard, matchlist=None):
        self._name = name
        self._uid = uid
        self._id = id
        self._shard = shard
        self._matches = matchlist

    @property
    def shard(self):
        return self._shard

    @property
    def uid(self):
        return self._uid

    @property
    def name(self):
        return self._name

    @property
    def id(self):
        return self._id

    @property
    def matches(self):
        return self._matches


class Telemetry:

    def __init__(self, telemetry, url=None, match=None):
        self._url = url
        self.tel = telemetry
        self._match = match
        self._damageEvents = []
        self._movements = []
        self.all = []
        self._attacks = []
        self._kills = []

    @property
    def url(self):
        return self._url

    @property
    def match(self):
        return self._match

    @property
    def full(self):
        return self.all

    def damage_events(self):
        """
        Gets all telemetry events in which damage was taken
        :return: List
        """
        if self._damageEvents:
            return self._damageEvents
        for item in self.tel:
            self.all.append(item)
            if item["_T"] == "LogPlayerTakeDamage":
                self._damageEvents.append(item)  # {"cause": })
        return self._damageEvents

    def movements(self):
        if self._movements:
            return self._movements
        for item in self.tel:
            if item["_T"] == "LogPlayerPosition":
                self._movements.append({"time": item["_D"], "name": item["character"]["name"],
                                        "position": {"x": item["character"]["location"]["x"],
                                                     "y": item["character"]["location"]["y"]}})
        return self._movements

    def attacks(self):
        for item in self.tel:
            if item.get("attackId") is not None:
                self._attacks.append(item)
        return self._attacks

    def kills(self):
        i = 1
        for item in self.tel:
            i = i + 1
            if item.get("attackId") is not None and item.get("killer") is not None:
                self._kills.append(item)
        return self._kills


class Team:

    def __init__(self, players, id, data):
        self.players = players
        self.tId = id
        self.json = data
        # add methods to fill in their place, and if they won or not.

    @property
    def id(self):
        return self.tId

    @property
    def players(self):
        return self.players

    @property
    def won(self):
        return self.won

    @property
    def place(self):
        return self.place


class Filter:

    def __init__(self, sort=None, length=None, offset=None, matchid=None, username=None, userid=None):
        # self.sort = sort
        self.length = length
        self.offset = offset
        self.matchid = matchid
        self.username = username
        self.userid = userid
        self.sorts = {}
        # if self.sort is not str():
        # self.sorts = self.sort

    @property
    def length(self):
        return self.length

    @property
    def sort(self):
        return self.sort

    @property
    def sorts(self):
        return self.sorts

    @property
    def offset(self):
        return self.offset

    @property
    def matchid(self):
        return self.matchid

    @property
    def username(self):
        return self.username

    @property
    def userid(self):
        return self.userid

    @length.setter
    def length(self, value):
        self._length = value

    @offset.setter
    def offset(self, value):
        self._offset = value

    @matchid.setter
    def matchid(self, value):
        self._matchid = value

    @username.setter
    def username(self, value):
        self._username = value

    @userid.setter
    def userid(self, value):
        self._userid = value

    @sorts.setter
    def sorts(self, value):
        self._sorts = value


class Stats:

    def __init__(self, inputs):
        self.kills = self.Kills(inputs)

    class Kills:

        def __init__(self, inputs):
            self.car = inputs["roadKills"]
            self.daily = inputs["dailyKills"]
            self.assists = inputs["assists"]
            self.weekly = inputs["weeklyKills"]
            self.team = inputs["teamKills"]
            self.total = inputs["kills"]  # shadows stats.kills

        @property
        def __repr__(self):
            return self.total
