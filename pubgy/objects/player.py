class Player:

    def __init__(self, name, pId, uid, stats, shard, matchlist=None):
        self._name = name
        self._uid = uid
        self.pId = pId
        self._shard = shard
        self._matches = matchlist

    def __repr__(self):
        return self.pId

    @property
    def shard(self):
        return self._shard

    @property
    def uid(self):
        return self._uid

    @property
    def name(self):
        return self._name

    @property
    def matches(self):
        return self._matches
