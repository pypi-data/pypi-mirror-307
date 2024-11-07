"""unionrecursive.py
Unions a mapping object and its contained mappings within another mapping.
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
from copy import deepcopy
from collections.abc import Mapping
from typing import Any

# Third-Party Packages #

# Local Packages #
from .updaterecursive import update_recursive


# Definitions #
# Functions #
def union_recursive(d: Mapping, other: Mapping) -> Mapping:
    """Unions a mapping object and its contained mappings within another mapping.

    Args:
        d: The mapping type to union recursively.
        other: The other mapping to union with.

    Returns:
        A new mapping as the union of the two mappings recursively.
    """
    return update_recursive(deepcopy(d), other)
