"""parameters.py
A dataclass (NamedTuple) that holds parameters for any function.
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
from collections.abc import Iterable, Mapping
from typing import Any, NamedTuple

# Third-Party Packages #

# Local Packages #


# Definitions #
# Classes #
class Parameters(NamedTuple):
    """A named tuple for holding the parameters of a function."""

    # Attributes #
    args: Iterable[Any] = tuple()
    kwargs: Mapping[str, Any] = dict()
