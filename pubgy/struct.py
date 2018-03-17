class Shard:
    def __init__(self, name, id):
        """
        :param name: Shard name
        :type name: str
        :param id: ID of the shard
        :type id: str
        """
        self.same = name
        self.sid = id

    @property
    def name(self):
        return self.same

    @property
    def id(self):
        return self.sid


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

    def __init__(self, name, id, stats, shard):
        self.plyname = name
        self.plyid = id
        self.stats = stats
        self.shardId = shard

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
