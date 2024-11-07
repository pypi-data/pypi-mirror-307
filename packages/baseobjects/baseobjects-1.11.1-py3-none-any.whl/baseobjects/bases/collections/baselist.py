"""baselist.py
An abstract class that is a mixin of UserList and BaseObject.
"""
# Package Header #
from ...header import *

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__


# Imports #
# Standard Libraries #
from collections import UserList
from collections.abc import Iterable
from typing import Any

# Third-Party Packages #

# Local Packages #
from ..baseobject import BaseObject


# Definitions #
# Classes #
class BaseList(BaseObject, UserList):
    """An abstract class that is a mixin of UserList and BaseObject."""

    __slots__: str | Iterable[str] = {"data"}

    # Magic Methods #
    # Construction/Destruction
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        # Parent Attributes #
        super().__init__(*args, **kwargs)
        UserList.__init__(self)
