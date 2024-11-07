"""timezoneoffset.py
A function that gets the offset of a give timezone.
"""
# Package Header #
from ..header import *

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__


# Imports #
# Standard Libraries #
from datetime import datetime, timedelta, tzinfo

# Third-Party Packages #

# Local Packages #


# Definitions #
# Constants
INIT_DATE = datetime(1970, 1, 1)


# Functions #
def timezone_offset(tz: tzinfo) -> timedelta:
    """Gets the offset of the given timezone.

    Args:
        tz: The timezone to get the offset from.

    Returns:
        The time delta offset of the given timezone.
    """
    return tz.utcoffset(INIT_DATE)
