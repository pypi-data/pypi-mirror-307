"""updaterecursive.py
Updates a mapping object and its contained mappings based on another mapping.
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
from collections.abc import Mapping, Iterable

# Third-Party Packages #

# Local Packages #


# Definitions #
# Functions #
def _update_recursive(d: Mapping, updates: Mapping) -> Mapping:
    """Updates a mapping object and its contained mappings based on another mapping.

    Args:
        d: The mapping type to update recursively.
        updates: The mapping updates.

    Returns:
        The original mapping that has been updated.
    """
    d.update(
        (key, update_recursive(d.get(key, {}), value) if isinstance(value, Mapping) else value)
        for key, value in updates.items()
    )
    return d


def update_recursive(d: Mapping, updates: Iterable | Mapping) -> Mapping:
    """Updates a mapping object and its contained mappings based on another mapping.

    Args:
        d: The mapping type to update recursively.
        updates: The mapping updates.

    Returns:
        The original mapping that has been updated.
    """
    if isinstance(updates, Mapping):
        updates = updates.items()

    d.update(
        (key, _update_recursive(d.get(key, {}), value) if isinstance(value, Mapping) else value)
        for key, value in updates
    )
    return d
