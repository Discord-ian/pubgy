class Match:

    def __init__(self, id: object, tel: object, partis: object, shard: object) -> object:
        """
        :param id: The ID of the Match
        :type id: str
        :param tel: A link to the telemetry.json file
        :type tel: str
        :param partis: A list of Player objects
        :type partis: List
        :param shard: A shard object.
        """
        self.matchID = id
        self.tel = tel
        self.partis = partis
        self.shardId = shard
        # make a way to make a list of the Player class with everyone who was in the game.



    @property
    def id(self):
        return self.matchID

    @property
    def players(self):
        return self.partis

    @property
    def telemetry(self):
        return Telemetry(self.tel)

    @property
    def winner(self):
        return "Winner:"  # temporary

    @property
    def shard(self):
        return self.shardId


class Player:

    def __init__(self, name, id, stats, shard, uid):
        self.plyname = name
        self.plyid = id
        self.stats = stats
        self.uid = uid
        self.shardId = shard

    @property
    def uid(self):
        return self.uid

    @property
    def shard(self):
        return self.shardId

    @property
    def name(self):
        return self.plyname

    @property
    def id(self):
        return self.plyid


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

    def __init__(self, sort, length, offset, matchid=None, username=None, userid=None):
        self.sort = sort
        self.length = length
        self.offset = offset
        self.matchid = matchid
        self.username = username
        self.userid = userid
        self.sorts = {}
        if self.sort != String():
            for item in self.sort:
                self.sorts["sort"]
        else:
            self.sorts.append(self.sort)


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
