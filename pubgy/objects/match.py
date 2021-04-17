from pubgy.constants import MATCH_TYPES, MAP_LIST, GAME_MODES
from pubgy.objects.telemetry import Telemetry


class Match:
    """
    A Match object
    Returned whenever :func:`pubgy.client.matches` is called.
    """

    def __init__(self, matchID, participants, shard, winners, telemetry, map, matchType=None, gameMode=None):
        # TODO: matchType != gameMode
        """
        :param matchID: The match id
        :type matchID: str
        :param participants:  A list of :class:`objects.Player`
        :type participants: list
        :param shard: Which shard did the match occur on
        :type shard: list
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
        self.matchID = matchID
        self.participants = participants
        self.shardId = shard
        self.tel = Telemetry(url=telemetry)
        if matchType in MATCH_TYPES:
            self.matchType = matchType
        else:
            self.matchType = "Unknown Match Type"
            # TODO: Either raise exception of InvalidMatchType or pass through 'Unknown Match Type'
        self.winner = winners
        self._map = MAP_LIST[map]
        self.gameMode = GAME_MODES[gameMode]
        # make a way to make a list of the Player class with everyone who was in the game.

    def __repr__(self):
        return self.matchID

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
        """  # TODO: this will always be a list (and will have to because of console cross platform play)
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
