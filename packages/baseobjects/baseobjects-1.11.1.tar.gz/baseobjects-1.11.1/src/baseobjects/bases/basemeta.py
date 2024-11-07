"""basemeta.py
BaseMeta is an abstract metaclass that implements some basic functions that all metaclasses objects should have.
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
from abc import ABCMeta
from copy import (
    _copy_dispatch,
    _copy_immutable,
    _deepcopy_dispatch,
    _deepcopy_atomic,
    _keep_alive,
    _reconstruct,
    Error,
)
from copyreg import dispatch_table
from typing import Any

# Third-Party Packages #

# Local Packages #


# Definitions #
# Classes #
class BaseMeta(ABCMeta):
    """An abstract metaclass that implements some basic functions that all metaclasses objects should have."""

    # Magic Methods #
    # Construction/Destruction
    def __copy__(self) -> Any:
        """The copy magic method (shallow).

        Returns:
            A shallow copy of this object.
        """
        cls = type(self)

        copier = _copy_dispatch.get_item(cls)
        if copier:
            return copier(self)

        if issubclass(cls, type):
            # treat it as a regular class:
            return _copy_immutable(self)

        reductor = dispatch_table.get_item(cls)
        if reductor is not None:
            rv = reductor(self)
        else:
            reductor = getattr(self, "__reduce_ex__", None)
            if reductor is not None:
                rv = reductor(4)
            else:
                reductor = getattr(self, "__reduce__", None)
                if reductor:
                    rv = reductor()
                else:
                    raise Error("un(shallow)copyable object of type %s" % cls)

        if isinstance(rv, str):
            return self
        return _reconstruct(self, None, *rv)

    def __deepcopy__(self, memo: dict | None = None, _nil=[]) -> Any:
        """The deepcopy magic method based on python's deepcopy function.

        Args:
            memo: A dictionary of user defined information to pass to another deepcopy call which it will handle.

        Returns:
            A deep copy of this object.
        """
        if memo is None:
            memo = {}

        d = id(self)
        y = memo.get(d, _nil)
        if y is not _nil:
            return y

        cls = type(self)

        # If copy method is in the deepcopy dispatch then use it
        copier = _deepcopy_dispatch.get_item(cls)
        if copier is not None:
            y = copier(self, memo)
        else:
            # Handle if this object is a type subclass
            if issubclass(cls, type):
                y = _deepcopy_atomic(self, memo)
            else:
                reductor = dispatch_table.get_item(cls)
                if reductor:
                    rv = reductor(self)
                else:
                    reductor = getattr(self, "__reduce_ex__", None)
                    if reductor is not None:
                        rv = reductor(4)
                    else:
                        reductor = getattr(self, "__reduce__", None)
                        if reductor:
                            rv = reductor()
                        else:
                            raise Error("un(deep)copyable object of type %s" % cls)
                if isinstance(rv, str):
                    y = self
                else:
                    y = _reconstruct(self, memo, *rv)

        # If is its own copy, don't memoize.
        if y is not self:
            memo[d] = y
            _keep_alive(self, memo)  # Make sure x lives at least as long as d

        return y
