import asyncio
from .http import Query


class Pubgy:

    def __init__(self, auth_token):
        self.auth = auth_token
        self.loop = asyncio.get_event_loop()
        self.web = Query(self.loop, self.auth)

