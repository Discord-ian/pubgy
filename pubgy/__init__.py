__title__ = "PUBGy"
__author__ = "Discordian"
__license__ = "GNU"
__version__ = "2.0.0a"  # Different whole numbers signify major changes
# Letters indicate how new or stable it is.

from .client import *
from .http import Query
from .struct import Match, Player, Team, Filter
from .constants import *
from .utils.filter import *
