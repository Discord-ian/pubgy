class InvalidShard(Exception):
    pass


class PUBGError(Exception):

    def __init__(self, msg="Some error occurred with your request", *args, **kwargs):
        super().__init__(msg)


class ResourceNotFound(PUBGError):
    pass


class InvalidAPIKey(PUBGError):
    pass


class InvalidPlayerID(PUBGError):
    pass

class InvalidObject(Exception):

    pass
