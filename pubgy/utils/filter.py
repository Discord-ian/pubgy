import asyncio
from pubgy.objects import Filter

def newfilter(sort=None, length=None, offset=None, matchid=None, username=None, userid=None):
    if length == None:
        length = 5
    if offset == None:
        offset = 0
    return Filter(sort=sort, length=length, offset=offset, matchid=matchid, username=username, userid=userid)
