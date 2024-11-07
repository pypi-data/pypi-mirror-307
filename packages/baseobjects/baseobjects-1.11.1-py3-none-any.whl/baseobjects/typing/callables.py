"""callables.py
Type hints for callables.
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
from collections.abc import Callable
from typing import Any

# Third-Party Packages #

# Local Packages #


# Definitions #
# Types #
# Callables
AnyCallable = Callable[..., Any]
AnyCallableType = Callable[..., type[Any]]

# Objects
GetObjectMethod = Callable[[Any, Any, type[Any] | None, ...], "BaseMethod"]

# Getters, Setters, and Deletes
GetterMethod = Callable[[Any], Any]
SetterMethod = Callable[[Any, str], None]
DeleteMethod = Callable[[Any], None]
PropertyCallbacks = tuple[GetterMethod, SetterMethod, DeleteMethod]

# Available Types
__all__ = [
    "AnyCallable",
    "AnyCallableType",
    "GetObjectMethod",
    "GetterMethod",
    "SetterMethod",
    "DeleteMethod",
    "PropertyCallbacks",
]
