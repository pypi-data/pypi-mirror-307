"""singlekwargdispatch.py
Extends singledispatch to allow kwargs to be used for dispatching.

The normal single dispatching requires at least one arg for dispatching. This object retains this functionality, but
allows the first kwarg to be used for dispatching if no args are provided. Furthermore, a kwarg name can be
specified to have the dispatcher use that kwarg instead of the first kwarg.
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
from functools import singledispatch, singledispatchmethod, update_wrapper
from types import NoneType
from typing import Any

# Third-Party Packages #

# Local Packages #
from ..typing import AnyCallable
from .dynamiccallable import DynamicMethod
from .basedecorator import BaseDecorator
from .callablemultiplexer import MethodMultiplexer


# Definitions #
# Classes #
class singlekwargdispatchmethod(DynamicMethod):
    """A wrapper for a bound singlekwargsipatch."""

    # Attributes #
    _call_method: str = "dispatch_call"

    # Calling
    def dispatch_call(self, *args: Any, **kwargs: Any) -> Any:
        """Calls the wrapped function's dispatch methods and returns the result.

        Args:
            *args: The arguments of the wrapped function.
            **kwargs: The keyword arguments of the wrapped function.

        Returns:
            The output of the wrapped function.
        """
        method = self.__func__.dispatcher.dispatch(self.__func__.parse(*args, **kwargs))
        return method.__get__(self.__self__, self.__owner__)(*args, **kwargs)


class singlekwargdispatch(BaseDecorator, singledispatchmethod):
    """Extends singledispatch to allow kwargs to be used for dispatching.

    The normal single dispatching requires at least one arg for dispatching. This object retains this functionality, but
    allows the first kwarg to be used for dispatching if no args are provided. Furthermore, a kwarg name can be
    specified to have the dispatcher use that kwarg instead of the first kwarg.

    Attributes:
        _kwarg: The name of the kwarg to use of parsing the args for the class to use for dispatching.
        _parse_method: The default method for parsing the args for the class to use for dispatching.
        parse: The method for parsing the args for the class to use for dispatching.
        dispatcher: The single dispatcher to use for this object.

    Args:
        kwarg: Either the name of kwarg to dispatch with or the method to wrap.
        func: The func to wrap.
        *args: Arguments for inheritance.
        init: Determines if this object will construct.
        **kwargs: Keyword arguments for inheritance.
    """

    # Attributes #
    method_type: type[DynamicMethod] = singlekwargdispatchmethod
    _bind_method: str = "bind_method_dispatcher"

    _kwarg: str | None = None
    _parse_method: str = "parse_first"
    parse: MethodMultiplexer
    dispatcher: AnyCallable | None = None

    # Properties #
    @property
    def kwarg(self) -> str | None:
        """The name of the kwarg to get the class for the dispatching."""
        return self._kwarg

    @kwarg.setter
    def kwarg(self, value: str | None) -> None:
        self.set_kwarg(kwarg=value)

    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        kwarg: AnyCallable | str | None = None,
        func: AnyCallable | None = None,
        *args: Any,
        wrapper_method: str | None = None,
        init: bool = True,
        **kwargs: Any,
    ) -> None:
        # New Attributes #
        self.parse: MethodMultiplexer = MethodMultiplexer(instance=self, select=self._parse_method)

        # Parent Attributes #
        super().__init__(*args, init=False, **kwargs)

        # Object Creation #
        if init:
            if isinstance(kwarg, str):
                self.construct(kwarg=kwarg, func=func, wrapper_method=wrapper_method)
            else:
                self.construct(func=kwarg, wrapper_method=wrapper_method)

    # Pickling
    def __getstate__(self) -> dict[str, Any]:
        """Creates a dictionary of attributes which can be used to rebuild this object

        Returns:
            A dictionary of this object's attributes.
        """
        state = super().__getstate__()
        state["parse"] = (self.parse.register, self.parse.selected)
        return state

    def __setstate__(self, state: dict[str, Any]) -> None:
        """Builds this object based on a dictionary of corresponding attributes.

        Args:
            state: The attributes to build this object from.
        """
        self.__dict__.update(state)
        s, r = state["parse"]
        self.parse = MethodMultiplexer(instance=self, select=s, register=r)

    # Instance Methods #
    # Constructors
    def construct(
        self,
        kwarg: AnyCallable | str | None = None,
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
        if kwarg is not None:
            self.kwarg = kwarg

        if func is not None:
            self.dispatcher = singledispatch(func)

        super().construct(func=func, *args, **kwargs)

        if self.dispatcher is not None:
            self.call_method = "dispatch_call"

    # Setters
    def set_kwarg(self, kwarg: str | None) -> None:
        """Sets the name of the kwarg for dispatching and changes the arg parsing to check for the kwarg.

        Args:
            kwarg: The name of the kwarg or None for checking the first kwarg.
        """
        if kwarg is None:
            self.parse.select("parse_first")
        else:
            self.parse.select("parse_kwarg")
        self._kwarg = kwarg

    # Parameter Parsers
    def parse_first(self, *args: Any, **kwargs: Any) -> type[Any]:
        """Parses input for the first arg or the first kwarg's class to be used for dispatching.

        Args:
            *args: The args given to the method.
            **kwargs: The kwargs given to the method.

        Returns:
            The class to be used for dispatching.
        """
        if args:
            return args[0].__class__
        else:
            try:
                return next(iter(kwargs.values())).__class__
            except StopIteration:
                return NoneType

    def parse_kwarg(self, *args: Any, **kwargs: Any) -> type[Any]:
        """Parses input for the first arg or a specific kwarg's class to be used for dispatching.

        Args:
            *args: The args given to the method.
            **kwargs: The kwargs given to the method.

        Returns:
            The class to be used for dispatching.
        """
        return args[0].__class__ if args else kwargs.get(self._kwarg, None).__class__

    # Binding
    def bind_method_dispatcher(self, instance: Any = None, owner: type[Any] | None = None) -> AnyCallable:
        """Creates a function which dispatches the correct bound method based on the input.

        Args:
            instance: The object to bind this object to.
            owner: The class of the object being bound to.

        Returns:
            A function which dispatches the correct bound method.
        """
        if instance is None:
            return self

        if isinstance(self.__wrapped__, classmethod):
            def dispatch_function(self_, *args, **kwargs):
                method = self.dispatcher.dispatch(self.parse(*args, **kwargs))
                return method.__get__(None, self_)(*args, **kwargs)
        else:
            def dispatch_function(self_, *args, **kwargs):
                method = self.dispatcher.dispatch(self.parse(*args, **kwargs))
                return method.__get__(self_)(*args, **kwargs)

        dispatch_function.__isabstractmethod__ = getattr(self.__wrapped__, '__isabstractmethod__', False)
        dispatch_function.register = self.register
        update_wrapper(dispatch_function, self.__wrapped__)
        if isinstance(self.__wrapped__, classmethod):
            dispatch_function = classmethod(dispatch_function)
        return dispatch_function.__get__(instance, owner)

    # Method Dispatching
    def dispatch_call(self, *args: Any, **kwargs: Any) -> Any:
        """Parses input to decide which method to use in the register.

        Args:
            *args: The arguments to pass to the found method.
            **kwargs: The keyword arguments to pass to the found method.

        Returns:
            The return of the found method.
        """
        return self.dispatcher.dispatch(self.parse(*args, **kwargs))(*args, **kwargs)
