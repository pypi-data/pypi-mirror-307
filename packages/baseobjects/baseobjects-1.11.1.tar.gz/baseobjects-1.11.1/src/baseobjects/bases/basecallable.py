"""basecallable.py
An abstract class which implements the basic structure for creating functions and methods.
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
from asyncio.coroutines import iscoroutinefunction, _is_coroutine
from collections.abc import Iterable
from functools import WRAPPER_ASSIGNMENTS
from typing import Any
from types import FunctionType, MethodType
import weakref

# Third-Party Packages #

# Local Packages #
from ..typing import AnyCallable, GetObjectMethod
from .baseobject import BaseObject


# Definitions #
# Classes #
class BaseCallable(BaseObject):
    """An abstract class which implements the basic structure for creating a callable.

    Attributes:
        __wrapped__: The function to wrap.

    Args:
        func: The function to wrap.
        *args: Arguments for inheritance.
        init: Determines if this object will construct.
        **kwargs: Keyword arguments for inheritance.
    """

    # Attributes #
    __wrapped__: AnyCallable | None = None
    _is_coroutine: object | None = None
    _cast_excluded: set = {"__call__"}

    # Properties #
    @property
    def __func__(self) -> AnyCallable:
        """The function which this callable wraps."""
        return self.__wrapped__

    @__func__.setter
    def __func__(self, value: AnyCallable | None) -> None:
        if value is not None and not callable(value) and not hasattr(value, "__get__"):
            raise TypeError(f"{value!r} is not callable or a descriptor")

        self.__wrapped__ = value

        if value is None:
            self._is_coroutine = None
        else:
            self._is_coroutine = _is_coroutine if iscoroutinefunction(value) else None
            d_copy = getattr(value, "__dict__", {}).copy()
            # Copy all attributes from the wrapped function to this object.
            if d_copy:
                exlcuded = set(dir(self))
                for k, v in d_copy.items():
                    if k not in exlcuded:
                        setattr(self, k, v)
            # Assign documentation from warped function to this object.
            for attr in WRAPPER_ASSIGNMENTS:
                try:
                    value = getattr(value, attr)
                except AttributeError:
                    pass
                else:
                    setattr(self, attr, value)

    @property
    def __name__(self) -> str:
        """The name of the function this object is wrapping."""
        return "" if self.__wrapped__ is None else self.__wrapped__.__name__

    @property
    def is_coroutine(self) -> bool:
        """Determines if the wrapped function is a coroutine."""
        return self._is_coroutine is not None

    # Magic Methods #
    # Construction/Destruction
    def __new__(cls, func: AnyCallable | None = None, *args: Any, **kwargs: Any) -> "BaseCallable":
        """Dispatches either an unbound instance or a bound instance if the given function is a method.

        Args:
            func: The function or method to wrap.
            *args: The arguments for building an instance.
            **kwargs: The keyword arguments for build an instance.
        """
        new_callable = super().__new__(cls)
        if (instance := getattr(func, "__self__", None)) is not None:
            new_callable.__init__(func, *args, **kwargs)
            new_callable = new_callable.__get__(instance, instance.__class__)

        return new_callable

    def __init__(
        self,
        func: AnyCallable | None = None,
        *args: Any,
        init: bool = True,
        **kwargs: Any,
    ) -> None:
        # Parent Attributes #
        super().__init__(*args, init=False, **kwargs)

        # Object Construction #
        if init:
            self.construct(func=func, *args, **kwargs)

    # Calling
    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """Calls the wrapped function with the instance as an argument.

        Args:
            *args: The arguments of the wrapped function.
            **kwargs: The keyword arguments of the wrapped function.

        Returns:
            The output of the wrapped function.
        """
        return self.__wrapped__(*args, **kwargs)

    # Instance Methods #
    # Constructors/Destructors
    def construct(
        self,
        func: AnyCallable | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """The constructor for this object.

        Args:
            func: The function to wrap.
            *args: Arguments for inheritance.
            **kwargs: Keyword arguments for inheritance.
        """
        if func is not None:
            self.__func__ = func

        super().construct(*args, **kwargs)

    # Casting
    def as_function(self) -> FunctionType:
        """Creates a wrapper function of this class."""
        if self._is_coroutine:
            async def wrapper_function(*args: Any, **kwargs: Any) -> Any:
                """A function which wraps a callable."""
                return await self(*args, **kwargs)
        else:
            def wrapper_function(*args: Any, **kwargs: Any) -> Any:
                """A function which wraps a callable."""
                return self(*args, **kwargs)

        for attr in WRAPPER_ASSIGNMENTS:
            try:
                value = getattr(self, attr)
            except AttributeError:
                pass
            else:
                setattr(wrapper_function, attr, value)

        wrapper_function.__dict__.update(self.__dict__)
        wrapper_function.__wrapped__ = self

        wrapper_dict =  wrapper_function.__dict__
        for n in (n for n in self._cast_excluded if n in wrapper_dict):
            del wrapper_dict[n]

        return wrapper_function


class BaseMethod(BaseCallable):
    """An abstract class which implements the basic structure for creating methods.

    Attributes:
        _self_: A weak reference to the object to bind this object to.
        __owner__: The class owner of the object.
        _binding: Determines if this callable will bind the function to the contained object.

    Args:
        func: The function to wrap.
        instance: The other object to bind this method to.
        owner: The class of the other object to bind this method to.
        *args: Arguments for inheritance.
        init: Determines if this object will construct.
        **kwargs: Keyword arguments for inheritance.
    """

    # Attributes #
    _self_: weakref.ref | None = None
    __owner__: type[Any] | None = None

    _binding: bool = True

    # Properties #
    @property
    def __self__(self) -> Any:
        """The object to bind this object to."""
        try:
            return self._self_()
        except TypeError:
            return None

    @__self__.setter
    def __self__(self, value: Any) -> None:
        self._self_ = None if value is None else weakref.ref(value)

    # Calling
    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """Calls the wrapped function with the instance as an argument.

        Args:
            *args: The arguments of the wrapped function.
            **kwargs: The keyword arguments of the wrapped function.

        Returns:
            The output of the wrapped function.
        """
        return self.__wrapped__(self._self_(), *args, **kwargs)

    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        func: AnyCallable | None = None,
        instance: Any = None,
        owner: type[Any] | None = None,
        *args: Any,
        init: bool = True,
        **kwargs: Any,
    ) -> None:
        # Parent Attributes #
        super().__init__(*args, init=False, **kwargs)

        # Object Construction #
        if init:
            self.construct(func=func, instance=instance, owner=owner, *args, **kwargs)

    # Pickling
    def __getstate__(self) -> dict[str, Any]:
        state = super().__getstate__()
        state["_self_"] = self.__self__
        return state

    # Instance Methods #
    # Constructors/Destructors
    def construct(
        self,
        func: AnyCallable | None = None,
        instance: Any = None,
        owner: type[Any] | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """The constructor for this object.

        Args:
            func: The function to wrap.
            instance: The other object to bind this method to.
            owner: The class of the other object to bind this method to.
            *args: Arguments for inheritance.
            **kwargs: Keyword arguments for inheritance.
        """
        if instance is not None:
            self.__self__ = instance

        if owner is not None:
            self.__owner__ = owner

        super().construct(func=func, *args, **kwargs)

    # Binding
    def bind(self, instance: Any = None, owner: type[Any] | None = None) -> "BaseMethod":
        """Binds this object to another.

        Args:
            instance: The object to bind this object to.
            owner: The class of the object being bound to.

        Returns:
            This object.
        """
        if instance is not None:
            self.__self__ = instance
        if owner is not None:
            self.__owner__ = owner
        return self

    def bind_to_attribute(
        self,
        instance: Any = None,
        owner: type[Any] | None = None,
        name: str | None = None,
    ) -> "BaseMethod":
        """Creates a method of this function which is bound to another object and sets the method an attribute.

        Args:
            instance: The object to bind this object to.
            owner: The class of the object being bound to.
            name: The name of the attribute to set this object to. Default is the function name.

        Returns:
            This object.
        """
        if name is None:
            name = self.__wrapped__.__name__

        if instance is not None:
            self.__self__ = instance
        if owner is not None:
            self.__owner__ = owner
        setattr(instance, name, self)

        return self

    # Method Overrides #
    # Special method overriding which leads to less overhead.
    __get__: GetObjectMethod = bind


class BaseFunction(BaseCallable):
    """An abstract class which implements the basic structure for creating functions.

    Attributes:
        method_type: The type of method to create when binding.
    """

    # Attributes #
    method_type: type[BaseMethod] | None = BaseMethod

    # Instance Methods #
    # Binding
    def bind(self, instance: Any = None, owner: type[Any] | None = None) -> BaseCallable | BaseMethod:
        """Creates a method of this function which is bound to another object.

        Args:
            instance: The object to bind the method to.
            owner: The class of the object being bound to.

        Returns:
            The bound method of this function.
        """
        return self if instance is None else self.method_type(func=self, instance=instance, owner=owner)

    def bind_builtin(self, instance: Any = None, owner: type[Any] | None = None) -> BaseCallable | MethodType:
        """Creates a method of this function which is bound to another object using the builtin method.

        Args:
            instance: The object to bind the method to.
            owner: The class of the object being bound to.

        Returns:
            The bound method of this function.
        """
        return self if instance is None else MethodType(self, instance)

    def bind_to_attribute(
        self,
        instance: Any = None,
        owner: type[Any] | None = None,
        name: str | None = None,
    ) -> BaseCallable | BaseMethod:
        """Creates a method of this function which is bound to another object and sets the method an attribute.

        Args:
            instance: The object to bind the method to.
            owner: The class of the object being bound to.
            name: The name of the attribute to set the method to. Default is the function name.

        Returns:
            The bound method of this function.
        """
        if instance is None:
            return self

        if name is None:
            name = self.__wrapped__.__name__

        method = self.method_type(func=self, instance=instance, owner=owner)
        setattr(instance, name, method)

        return method

    # Method Overrides #
    # Special method overriding which leads to less overhead.
    __get__: GetObjectMethod = bind
