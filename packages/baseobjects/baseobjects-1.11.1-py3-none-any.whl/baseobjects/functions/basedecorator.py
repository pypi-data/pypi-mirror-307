"""basedecorator.py
An abstract class which implements the basic structure for creating decorators.
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
from typing import Any

# Third-Party Packages #

# Local Packages #
from ..typing import AnyCallable
from .dynamiccallable import DynamicFunction


# Definitions #
# Classes #
class BaseDecorator(DynamicFunction):
    """An abstract class which implements the basic structure for creating decorators."""

    # Attributes #
    _bind_method: str = "bind_builtin"
    _call_method: str = "construct_call"
    _wrapper_method: str = "call"

    # Properties
    @property
    def wrapper_method(self) -> str | None:
        """The name of the method which will act as the wrapper for this decorator."""
        return self._wrapper_method

    @wrapper_method.setter
    def wrapper_method(self, value: str) -> None:
        if self.call_method == self._wrapper_method:
            self.call_method = value
        self._wrapper_method = value

    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        func: AnyCallable | None = None,
        *args: Any,
        wrapper_method: str | None = None,
        init: bool = True,
        **kwargs: Any,
    ) -> None:
        # Parent Attributes #
        super().__init__(*args, init=False, **kwargs)

        # Object Construction #
        if init:
            self.construct(func=func, *args, wrapper_method=wrapper_method, **kwargs)

    # Instance Methods #
    # Constructors/Destructors
    def construct(
        self,
        func: AnyCallable | None = None,
        *args: Any,
        wrapper_method: str | None = None,
        **kwargs: Any,
    ) -> None:
        """The constructor for this object.

        Args:
            func: The function to wrap.
            *args: Arguments for inheritance.
            wrapper_method: The name of the method which will act as the wrapper for this decorator.
            **kwargs: Keyword arguments for inheritance.
        """
        if wrapper_method is not None:
            self.wrapper_method = wrapper_method

        if func is not None:
            self.call_method = self._wrapper_method

        super().construct(func, *args, **kwargs)

    # Calling
    def construct_call(
        self,
        func: AnyCallable | None = None,
        *args: Any,
        wrapper_method: str | None = None,
        **kwargs: Any,
    ) -> "BaseDecorator":
        """A method for constructing this object via this object being called.

        Args:
            func: The function or method to wrap.
            *args: The arguments from the call which can construct this object.
            wrapper_method: The name of the method which will act as the wrapper for this decorator.
            **kwargs: The keyword arguments from the call which can construct this object.

        Returns:
            This object.
        """
        self.construct(func=func, *args, wrapper_method=wrapper_method, **kwargs)
        instance = getattr(func, "__self__", None)
        return self if instance is None else self.__get__(instance, instance.__class__)
