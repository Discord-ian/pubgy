from pubgy.constants import *
class Match:

    def __init__(self, id, participants, shard, winners, telemetry, matchType=None):
        """
        :param id: The ID of the Match
        :type id: str
        :param partis: A list of Player objects
        :type partis: List
        :param shard: A shard object.
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
        # make a way to make a list of the Player class with everyone who was in the game.



    @property
    def id(self):
        return self.matchID

    @property
    def players(self):
        return self.participants

    @property
    def winners(self):
        return self.winner

    @property
    def shard(self):
        return self.shardId

    @property
    def telemetry(self):
        return self.tel

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

    def __init__(self, telemetry):
        self.tel = telemetry

    @property
    def url(self):
        return self.tel

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
        #self.sort = sort
        self.length = length
        self.offset = offset
        self.matchid = matchid
        self.username = username
        self.userid = userid
        self.sorts = {}
        #if self.sort is not str():
            #self.sorts = self.sort

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
