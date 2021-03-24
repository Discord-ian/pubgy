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
