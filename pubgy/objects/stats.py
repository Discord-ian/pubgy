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
