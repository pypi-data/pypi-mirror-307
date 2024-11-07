"""methodnames.py
Functions for getting method names from objects.
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
from collections.abc import Generator
from typing import Any

# Third-Party Packages #

# Local Packages #


# Definitions #
# Functions #
def iter_method_names(obj: Any) -> Generator[str, None, None]:
    """Creates an iterator which iterates over the method names of an object.

    Args:
        obj: The object to iterate the method names from.

    Returns:
        The iterator as a generator which iterates over the method names of an object.
    """
    return (name for name in dir(obj) if callable(getattr(obj, name, None)))


def iter_public_method_names(obj: Any) -> Generator[str, None, None]:
    """Creates an iterator which iterates over the public method names of an object.

    Args:
        obj: The object to iterate the public method names from.

    Returns:
        The iterator as a generator which iterates over the public method names of an object.
    """
    return (name for name in iter_method_names(obj) if name[0] != '_')


def get_method_names(obj: Any) -> tuple[str, ...]:
    """Gets the method names of an object.

    Args:
        obj: The object to get the method names from.

    Returns:
        The method names of an object.
    """
    return tuple(iter_method_names(obj))


def get_public_method_names(obj: Any) -> tuple[str, ...]:
    """Gets the public method names of an object.

    Args:
        obj: The object to get the public method names from.

    Returns:
        The public method names of an object.
    """
    return tuple(iter_public_method_names(obj))


