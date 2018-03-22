import asyncio
from pubgy.struct import Filter

def newfilter(sort, length=None, offset=None):
    if length == None:
        length = 5
    if offset == None:
        offset = 0
    return Filter(sort=sort, length=length, offset=offset)
