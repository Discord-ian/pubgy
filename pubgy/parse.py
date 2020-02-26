import json
from .http import Query, Route
from .constants import *
class Parser:
    def __init__(self, queryobj):
        """
        Must pass a valid Query object so it can make requests
        :param queryobj:
        """
        self.query = queryobj

#    async def telemetry(self, jsondata):

