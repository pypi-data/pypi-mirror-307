"""callablemultiplexer.py
Callables which select between either functions or methods to be used as the call method.
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
from asyncio import iscoroutinefunction
from typing import Any, NamedTuple, ClassVar
from types import MethodType
from warnings import warn

# Third-Party Packages #

# Local Packages #
from ..typing import AnyCallable, GetObjectMethod
from ..bases import BaseObject, BaseCallable, BaseMethod
from .functionregister import FunctionRegister


# Definitions #
# Classes #
class CallableMultiplexer(BaseMethod):
    """A callable which select between either functions or methods to be used as the call method.

    The CallableMultiplexer has a register which it uses to store the functions/methods to be multiplexed.
    Additionally, an object can be assigned and its methods will be part of the multiplex. Having the object being
    directly multiplexed allows more dynamic interaction as the object's methods may change during runtime. Note that
    the register's functions/methods take priority in selection.

    Attributes:
        register: The function register to use for selecting a function/method.
        _selected: The name of the function/method to select for use.
        is_binding: Determines if this callable will bind the selected function to a different object.
        is_self_bound: Determines if this callable will bind the selected function to the contained object, self.
        is_coroutine: Checks if this callable is a coroutine.

    Args:
        register: The function register to use for selecting a function/method.
        instance: An object to wrap which will be used to find functions/methods.
        owner: The class of the object used for finding functions/methods.
        select: The name of the function/method to select for use.
        binding: Determines if this object will bind the selected function as a method.
        *args: Arguments for inheritance.
        init: Determines if this object will construct.
        **kwargs: Keyword arguments for inheritance.
    """

    # Attributes #
    register: FunctionRegister | None = None
    _selected: str | None = None

    is_binding: bool = False
    is_self_bound: bool = False

    # Properties #
    @property
    def selected(self) -> str | None:
        """The name of the selected function/method."""
        return self._selected

    @selected.setter
    def selected(self, value: str) -> None:
        self.select(value)

    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        register: FunctionRegister | None = None,
        instance: Any = None,
        owner: type[Any] | None = None,
        select: str | None = None,
        binding: bool = False,
        *args: Any,
        init: bool = True,
        **kwargs: Any,
    ) -> None:
        # Parent Attributes #
        super().__init__(*args, init=False, **kwargs)

        # Object Construction #
        if init:
            self.construct(
                register=register,
                instance=instance,
                owner=owner,
                select=select,
                binding=binding,
                *args,
                **kwargs,
            )

    # Pickling
    def __getstate__(self) -> dict[str, Any]:
        state = super().__getstate__()
        del state["_self_"]
        warn("CallableMultiplexer Weak reference deleted for pickle, may not work as intended.")
        return state

    # Calling
    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """Calls the wrapped function with the instance as an argument if is_binding is True.

        Args:
            *args: The arguments of the wrapped function.
            **kwargs: The keyword arguments of the wrapped function.

        Returns:
            The output of the wrapped function.
        """
        if self.is_self_bound or self.is_binding:
            return self.__wrapped__.__get__(self._self_(), self.__owner__)(*args, **kwargs)
        else:
            return self.__wrapped__(*args, **kwargs)

    # Instance Methods #
    # Constructors/Destructors
    def construct(
        self,
        register: AnyCallable | None = None,
        instance: Any = None,
        owner: type[Any] | None = None,
        select: str | None = None,
        binding: bool | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """The constructor for this object.

        Args:
            register: The function register to use for selecting a function/method.
            instance: An object to wrap which will be used to find functions/methods.
            owner: The class of the object used for finding functions/methods.
            select: The name of the function/method to select for use.
            binding: Determines if this object will bind the selected function as a method.
            *args: Arguments for inheritance.
            **kwargs: Keyword arguments for inheritance.
        """
        if register is not None:
            self.register = register
        else:
            self.build_register()

        if binding is not None:
            self.is_binding = binding

        super().construct(instance=instance, owner=owner, *args, **kwargs)

        if select is not None:
            self.select(select)

    def build_register(self) -> None:
        """Creates the register this object will use for function/method selection."""
        self.register = FunctionRegister()

    # Register
    def add_function(self, name: str, func: BaseCallable) -> None:
        """Adds a function to the register.

        Args:
            name: The name of the function being added.
            func: The function to add to the register.
        """
        self.register[name] = func

    def add_method(self, name: str, method: BaseCallable) -> None:
        """Adds a method to the register.

        Args:
            name: The name of the method being added.
            method: The method to add to the register.
        """
        self.register[name] = getattr(method, "__func__")

    def bind_builtin_bypass(self, instance: Any = None, owner: type[Any] | None = None) -> BaseCallable | MethodType:
        """Creates a method of the selected function which is bound to another object using the builtin method.

        Args:
            instance: The object to bind the method to.
            owner: The class of the object being bound to.

        Returns:
            The bound method of this function.
        """
        return self if instance is None else MethodType(self.__wrapped__, instance)

    # Callable Selection
    def select(self, name: str | None) -> None:
        """Selects a function/method to use within the register or the wrapped object.

        Args:
            name: The name of function/method in the register or object to use.
        """
        if name is None:
            func = None
        elif (func := self.register.get(name, None)) is not None:
            self.is_self_bound = False
        elif self._self_() is not None:
            func = getattr(self._self_(), name)
            self.is_self_bound = True
        self.__func__ = func
        self._selected = name

    def add_select_function(self, name: str, func: BaseCallable) -> None:
        """Adds a function to the register and selects it.

        Args:
            name: The name of the function being added.
            func: The function to add to the register.
        """
        self.register[name] = self.__func__ = func
        self._selected = name

    def add_select_method(self, name: str, method: BaseCallable) -> None:
        """Adds a method to the register and selects it.

        Args:
            name: The name of the method being added.
            method: The method to add to the register.
        """
        self.register[name] = self.__func__ = getattr(method, "__func__")
        self._selected = name


class MethodMultiplexer(CallableMultiplexer):
    """A callable which only uses methods to be used as the call method.

    The MethodMultiplexer has a register which it uses to store the methods to be multiplexed. Additionally, an object
    can be assigned and its methods will part of multiplex. Having the object being directly multiplexed allows more
    dynamic interaction as the object's methods may change during runtime. Note that the register's methods take
    priority in selection.
    """

    # Magic Methods #
    # Calling
    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """Calls the wrapped function with the instance as an argument.

        Args:
            *args: The arguments of the wrapped function.
            **kwargs: The keyword arguments of the wrapped function.

        Returns:
            The output of the wrapped function.
        """
        return self.__wrapped__.__get__(self._self_(), self.__owner__)(*args, **kwargs)


class CallableMultiplexItem(NamedTuple):
    """A NamedTuple with specifications for a pickled MethodMultiplexer."""

    register: dict
    selected: str
    type: str


class CallableMultiplexObject(BaseObject):
    """An object which can be subclassed to allow MethodMultiplexer to be pickled."""

    # Class Attributes #
    _callable_multiplexers: ClassVar[dict[str, type[CallableMultiplexer]]] = {
        CallableMultiplexer.__name__: CallableMultiplexer,
        MethodMultiplexer.__name__: MethodMultiplexer,
    }

    # Magic Methods #
    # Pickling
    def __getstate__(self) -> dict[str, Any]:
        """Creates a dictionary of attributes which can be used to rebuild this object

        Returns:
            A dictionary of this object's attributes.
        """
        state = {}
        for k, i in super().__getstate__().items():
            if isinstance(i, CallableMultiplexer):
                state[k] = CallableMultiplexItem(i.register, i.selected, i.__class__.__name__)
            else:
                state[k] = i

        return state

    def __setstate__(self, state: dict[str, Any]) -> None:
        """Builds this object based on a dictionary of corresponding attributes.

        Args:
            state: The attributes to build this object from.
        """
        super().__setstate__(state)
        for k, i in state.items():
            if isinstance(i, CallableMultiplexItem):
                self.__dict__[k] = self._callable_multiplexers[i.type](
                    register=i.register,
                    instance=self,
                    select=i.selected,
                )
