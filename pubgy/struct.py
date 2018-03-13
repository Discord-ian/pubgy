class Shard:
    def __init__(self, name, id):
        self.same = name
        self.sid = id

    @property
    def name(self):
        return self.same

    @property
    def id(self):
        return self.sid


class Match:

    def __init__(self, id, tel, partis, shard):
        self.matchID = id
        self.tel = tel
        self.partis = partis
        self.shardID = shard
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
        return self.shardID


class Player:

    def __init__(self, name, id, stats, shard):
        self.plyname = name
        self.plyid = id
        self.stats = stats
        self.shard = shard

    @property
    def shard(self):
        return self.shard

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
