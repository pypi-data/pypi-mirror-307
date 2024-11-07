"""functionregister.py
A register which holds functions.
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
from collections.abc import Iterable
from typing import Any

# Third-Party Packages #

# Local Packages #
from ..typing import AnyCallable
from ..bases import BaseDict


# Definitions #
# Classes #
class FunctionRegister(BaseDict):
    """A register which holds functions.

    Args:
        functions: The functions and their keys to add to the register.
        object_: An object whose functions will be added to the register.
        objects: An iterable of objects whose functions will be added to the register.
        *args: Arguments for inheritance.
        init: Determines if this object will construct.
        **kwargs: Keyword arguments for inheritance.
    """

    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        functions: dict[str, AnyCallable] | None = None,
        object_: Any = None,
        objects: Iterable[Any, ...] = None,
        *args: Any,
        init: bool = True,
        **kwargs: Any,
    ) -> None:
        # Parent Attributes #
        super().__init__(*args, **kwargs)

        # Object Construction #
        if init:
            self.construct(functions=functions, object_=object_, objects=objects, *args, **kwargs)

    # Instance Methods #
    # Constructors/Destructors
    def construct(
        self,
        functions: dict[str, AnyCallable] | None = None,
        object_: Any = None,
        objects: Iterable[Any, ...] = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """The constructor for this object.

        Args:
            functions: The functions and their keys to add to the register.
            object_: An object whose functions will be added to the register.
            objects: An iterable of objects whose functions will be added to the register.
            *args: Arguments for inheritance.
            **kwargs: Keyword arguments for inheritance.
        """
        if object_ is not None:
            self.update_from_object(object_=object_)

        if objects is not None:
            self.update_from_objects(*objects)

        if functions is not None:
            self.update(functions)

        super().construct(*args, **kwargs)

    def update_from_object(self, object_: Any) -> None:
        """Updates the register with an object whose functions will be added to the register.

        Args:
            object_: The object whose functions will be added to the register.
        """
        for name in set(dir(object_)) | set(vars(object_).keys()):
            attr = getattr(object_, name, None)
            func = None if attr is None or not callable(attr) else attr.__func__ if hasattr(attr, "__func__") else attr
            if func is not None:
                self.data[name] = func

    def update_from_objects(self, *args: Any) -> None:
        """Updates the register with objects whose functions will be added to the register.

        Args:
            *args: The objects whose functions will be added to the register.
        """
        for object_ in args:
            self.update_from_object(object_=object_)
