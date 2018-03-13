class Match:

    def __init__(self, id, tel, partis):
        self.matchid = id
        self.tel = tel
        self.partis = partis
        # make a way to make a list of the Player class with everyone who was in the game.

    @property
    def id(self):
        return self.matchid

    @property
    def players(self):
        return self.partis

    @property
    def telemetry(self):
        return Telemetry(self.tel)

    @property
    def winner(self):
        return "Winner:" # temporary


class Player:

    def __init__(self, name, id, stats):
        self.plyname = name
        self.plyid = id
        self.stats = stats

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
