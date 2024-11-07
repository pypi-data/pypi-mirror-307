"""generic.py
Generic types.
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

# Third-Party Packages #

# Local Packages #
from typing import TypeVar


# Definitions #
# Types #
KeyType = TypeVar("_KT")  # Key type.
ValueType = TypeVar("_VT")
KT_co = TypeVar("_KT_co", covariant=True)
VT_co = TypeVar("_VT_co", covariant=True)

# Available Types
__all__ = [
    "KeyType",
    "ValueType",
    "KT_co",
    "VT_co",
]
