import json
from .http import Query, Route
from .constants import *
from .struct import Telemetry


class Parser:
    def __init__(self, queryobj):
        """
        Must pass a valid Query object so it can make requests
        :param queryobj:
        """
        self.query = queryobj

    async def telemetry(self, telemetry, match=None):
        url = Route(method="telemetry", url=telemetry)
        tel = await self.query.request(url)
        return Telemetry(url=telemetry, telemetry=tel, match=match)
