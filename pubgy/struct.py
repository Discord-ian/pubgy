class Match:

    def __init__(self, id, tel, partis):
        self.id = id
        self.tel = tel
        # make a way to make a list of the Player class with everyone who was in the game.

    @property
    def id(self):
        return self.id

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
        self.name = name
        self.id = id
        self.stats = stats

    @property
    def name(self):
        return self.name

    @property
    def id(self):
        return self.id


class Telemetry:

    def __init__(self, telemetry):
        self.tel = telemetry

    @property
    def url(self):
        return self.tel
