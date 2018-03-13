__title__ = "PUBGy"
__author__ = "Discordian"
__license__ = "GNU"
__version__ = "1.0a" # Different whole numbers signify major changes
# Letters indicate how new or stable it is.

from .pubgy import Pubgy
from .http import Query
from .struct import Match, Player

import logging

logging.basicConfig(level=logging.INFO)



