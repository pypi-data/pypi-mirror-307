"""filetimetodatetime.py
A function to convert a filetime to a datetime.
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
FILETIME_INIT_DATE = datetime(1601, 1, 1, tzinfo=timezone.utc)  # The initial date of Filetime.


# Functions #
@singledispatch
def filetime_to_datetime(timestamp: int | float | str | bytes, tzinfo: tzinfo | None = timezone.utc) -> datetime:
    """Converts a filetime to a datetime object.

    Args:
        timestamp: The filetime to convert to a datetime.
        tzinfo: The timezone of the datetime.

    Returns:
        The datetime of the filetime.
    """
    raise TypeError(f"{timestamp.__class__} cannot be converted to a datetime")


@filetime_to_datetime.register
def _filetime_to_datetime(timestamp: int, tzinfo: tzinfo | None = None) -> datetime:
    """Converts a filetime to a datetime object.

    Args:
        timestamp: The filetime to convert to a datetime.
        tzinfo: The timezone of the datetime.

    Returns:
        The datetime of the filetime.
    """
    if tzinfo is None:
        return FILETIME_INIT_DATE.replace(tzinfo=tzinfo) + timedelta(microseconds=timestamp)
    else:
        return (FILETIME_INIT_DATE + timedelta(microseconds=timestamp)).astimezone(tz=tzinfo)


@filetime_to_datetime.register(float)
@filetime_to_datetime.register(str)
def _filetime_to_datetime(timestamp: float | str, tzinfo: tzinfo | None = None) -> datetime:
    """Converts a filetime to a datetime object.

    Args:
        timestamp: The filetime to convert to a datetime.
        tzinfo: The timezone of the datetime.

    Returns:
        The datetime of the filetime.
    """
    if tzinfo is None:
        return FILETIME_INIT_DATE.replace(tzinfo=tzinfo) + timedelta(microseconds=int(timestamp) / 10)
    else:
        return (FILETIME_INIT_DATE + timedelta(microseconds=int(timestamp) / 10)).astimezone(tz=tzinfo)


@filetime_to_datetime.register(bytes)
def _filetime_to_datetime(timestamp: bytes, tzinfo: tzinfo | None = None) -> datetime:
    """Converts a filetime to a datetime object.

    Args:
        timestamp: The filetime to convert to a datetime.
        tzinfo: The timezone of the datetime.

    Returns:
        The datetime of the filetime.
    """
    delta = timedelta(microseconds=int.from_bytes(timestamp, "little") / 10)
    if tzinfo is None:
        return FILETIME_INIT_DATE.replace(tzinfo=tzinfo) + delta
    else:
        return (FILETIME_INIT_DATE + delta).astimezone(tz=tzinfo)
