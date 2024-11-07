"""methodregister.py
A register which holds Methods.
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
import weakref

# Third-Party Packages #

# Local Packages #
from ..typing import AnyCallable
from .functionregister import FunctionRegister


# Definitions #
# Classes #
class BaseMethodRegister(FunctionRegister):
    """An abstract register which holds methods.

    Args:
        methods: The functions and their keys to add to the register.
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
        methods: dict[str, AnyCallable] | None = None,
        object_: Any = None,
        objects: Iterable[Any, ...] = None,
        *args: Any,
        init: bool = True,
        **kwargs: Any,
    ) -> None:
        # Parent Attributes #
        super().__init__(*args, init=False, **kwargs)

        # Override Attributes #
        self.data: FunctionRegister = FunctionRegister()

        # Object Construction #
        if init:
            self.construct(methods=methods, object_=object_, objects=objects, *args, **kwargs)

    @property
    def __func__(self) -> FunctionRegister:
        """The FunctionRegister this MethodRegister is wrapping."""
        return self.data

    @__func__.setter
    def __func__(self, value: FunctionRegister) -> None:
        self.data = value

    # Instance Methods #
    # Constructors/Destructors
    def construct(
        self,
        methods: dict[str, AnyCallable] | None = None,
        object_: Any = None,
        objects: Iterable[Any, ...] = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """The constructor for this object.

        Args:
            methods: The functions and their keys to add to the register.
            object_: An object whose functions will be added to the register.
            objects: An iterable of objects whose functions will be added to the register.
            *args: Arguments for inheritance.
            **kwargs: Keyword arguments for inheritance.
        """
        super().construct(functions=methods, object_=object_, objects=objects, *args, **kwargs)


class BoundMethodRegister(BaseMethodRegister):
    """A BaseMethodRegister which is bound to another object.

    Args:
        register: The BaseMethodRegister which this object wraps.
        instance: The other object to bind this register to.
        owner: The class of the other object to bind this register to.
        *args: Arguments for inheritance.
        init: Determines if this object will construct.
        **kwargs: Keyword arguments for inheritance.
    """

    # Attributes #
    _self_: weakref.ref | None = None
    __owner__: type[Any] | None = None

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

    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        register: BaseMethodRegister | None = None,
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
            self.construct(register=register, instance=instance, owner=owner, *args, **kwargs)

    # Instance Methods #
    # Constructors/Destructors
    def construct(
        self,
        register: BaseMethodRegister | None = None,
        instance: Any = None,
        owner: type[Any] | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """The constructor for this object.

        Args:
            register: The BaseMethodRegister which this object wraps.
            instance: The other object to bind this register to.
            owner: The class of the other object to bind this register to.
            *args: Arguments for inheritance.
            **kwargs: Keyword arguments for inheritance.
        """
        if register is not None:
            self.data = register.data

        if instance is not None:
            self.__self__ = instance

        if owner is not None:
            self.__owner__ = owner

        super().construct(*args, **kwargs)


class MethodRegister(BaseMethodRegister):
    """A register which holds functions and binds appropriately."""

    # Magic Methods #
    # Descriptor
    def __get__(self, instance: Any, owner: type[Any] | None = None) -> BoundMethodRegister:
        return BoundMethodRegister(register=self, instance=instance, owner=owner)
