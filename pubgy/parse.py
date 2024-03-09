"""
Copyright (c) 2018-2021 Discordian

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from .http import Query, Route
from .objects.telemetry import Telemetry
from .exceptions import InvalidObject


class Parser:
    def __init__(self, queryobj):
        """
        Must pass a valid Query object so it can make requests
        :param queryobj:
        """
        self.query = queryobj
        try:
            self.query.isquery
        except Exception:
            raise InvalidObject

    async def telemetry(self, telemetry, match=None):
        url = Route(method="telemetry", url=telemetry)
        tel = await self.query.request(url)
        return Telemetry(url=telemetry, telemetry=tel, match=match)
