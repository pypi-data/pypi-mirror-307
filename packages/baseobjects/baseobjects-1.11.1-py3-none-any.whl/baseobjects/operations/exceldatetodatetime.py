"""exceldatetodatetime.py
A function to convert an excel date to a datetime.
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
from datetime import datetime, timedelta, tzinfo, timezone
from functools import singledispatch

# Third-Party Packages #

# Local Packages #


# Definitions #
# Constants #
EXCEL_INIT_DATE = datetime(1899, 12, 30)  # The initial date of Filetime.


# Functions #
@singledispatch
def excel_date_to_datetime(timestamp: int | float | str | bytes, tzinfo: tzinfo | None = timezone.utc) -> datetime:
    """Converts a filetime to a datetime object.

    Args:
        timestamp: The filetime to convert to a datetime.
        tzinfo: The timezone of the datetime.

    Returns:
        The datetime of the filetime.
    """
    raise TypeError(f"{timestamp.__class__} cannot be converted to a datetime")


@excel_date_to_datetime.register(float)
@excel_date_to_datetime.register(int)
def _excel_date_to_datetime(timestamp: float | int, tzinfo: tzinfo | None = timezone.utc) -> datetime:
    """Converts a filetime to a datetime object.

    Args:
        timestamp: The filetime to convert to a datetime.
        tzinfo: The timezone of the datetime.

    Returns:
        The datetime of the filetime.
    """
    return EXCEL_INIT_DATE.replace(tzinfo=tzinfo) + timedelta(days=timestamp)


@excel_date_to_datetime.register(str)
@excel_date_to_datetime.register(bytes)
def _excel_date_to_datetime(timestamp: str | bytes, tzinfo: tzinfo | None = timezone.utc) -> datetime:
    """Converts a filetime to a datetime object.

    Args:
        timestamp: The filetime to convert to a datetime.
        tzinfo: The timezone of the datetime.

    Returns:
        The datetime of the filetime.
    """
    return EXCEL_INIT_DATE.replace(tzinfo=tzinfo) + timedelta(days=float(timestamp))
