class Team:

    def __init__(self, players, tId, data):
        self._players = players
        self.tId = tId
        self.json = data
        # add methods to fill in their place, and if they won or not.

    @property
    def id(self):
        return self.tId

    @property
    def players(self):
        return self._players

    @property
    def won(self):
        return self.won

    @property
    def place(self):
        return self.place
