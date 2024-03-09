class Filter:  # likely to remove

    def __init__(
        self,
        sort=None,
        length=None,
        offset=None,
        matchId=None,
        username=None,
        userid=None,
    ):
        # self.sort = sort
        self.length = length
        self.offset = offset
        self.matchId = matchId
        self.username = username
        self.userid = userid
        self.sorts = {}
        # if self.sort is not str():
        # self.sorts = self.sort

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
