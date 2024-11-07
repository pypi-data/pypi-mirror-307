"""timedcache.py
A cache that periodically resets and include its instantiation decorator function.
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
from collections.abc import Callable
from time import perf_counter
from typing import Any

# Third-Party Packages #

# Local Packages #
from ...typing import AnyCallable
from ...bases import search_sentinel
from ...collections import CircularDoublyLinkedContainer
from .basetimedcache import BaseTimedCacheCallable, BaseTimedCacheMethod, BaseTimedCache


# Definitions #
# Classes #
class TimedCacheCallable(BaseTimedCacheCallable):
    """A periodically clearing multiple item cache wrapper object for a function.

    Class Attributes:
        priority_queue_type = The type of priority queue to hold cache item priorities.

    Attributes:
        _maxsize: The number of results the cache will hold before replacing results.

        priority: The object that will control the replacement of cached results.

    Args:
        func: The function to wrap.
        maxsize: The max size of the cache.
        typed: Determines if the function's arguments are type sensitive for caching.
        lifetime: The period between cache resets in seconds.
        call_method: The default call method to use.
        local: Determines if the cache is local to each instance or all instances.
        *args: Arguments for inheritance.
        init: Determines if this object will construct.
        **kwargs: Keyword arguments for inheritance.
    """

    # Attributes #
    _cache_method: str = "unlimited_cache"
    _maxsize: int | None = None
    priority_queue_type: type[CircularDoublyLinkedContainer] = CircularDoublyLinkedContainer
    priority: Any

    # Properties #
    @property
    def maxsize(self) -> int:
        """The cache's max size and when updated it changes the cache to its optimal handle function."""
        return self._maxsize

    @maxsize.setter
    def maxsize(self, value: int) -> None:
        self.set_maxsize(value)

    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        func: AnyCallable | None = None,
        maxsize: int | None = None,
        typed: bool | None = None,
        lifetime: int | float | None = None,
        call_method: str | None = None,
        local: bool | None = None,
        *args: Any,
        init: bool = True,
        **kwargs: Any,
    ) -> None:
        # New Attributes #
        self.priority: Any = self.priority_queue_type()

        # Parent Attributes #
        super().__init__(*args, init=False, **kwargs)

        # Overriden Attributes #
        self.cache_container: dict = {}

        # Object Construction #
        if init:
            self.construct(
                func=func,
                lifetime=lifetime,
                maxsize=maxsize,
                typed=typed,
                call_method=call_method,
                local=local,
                *args,
                **kwargs,
            )

    # Container Methods
    def __len__(self) -> int:
        """The method that gets this object's length."""
        return self.get_length()

    # Instance Methods #
    # Constructors
    def construct(
        self,
        func: AnyCallable | None = None,
        maxsize: int | None = None,
        typed: bool = False,
        lifetime: int | float | None = None,
        call_method: str | None = None,
        local: bool = True,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """The constructor for this object.

        Args:
            func:  The function to wrap.
            maxsize: The max size of the cache.
            typed: Determines if the function's arguments are type sensitive for caching.
            lifetime: The period between cache resets in seconds.
            call_method: The default call method to use.
            local: Determines if the cache is local to each instance or all instances.
            *args: Arguments for inheritance.
            **kwargs: Keyword arguments for inheritance.
        """
        if maxsize is not None:
            self.maxsize = maxsize

        super().construct(
            func=func,
            typed=typed,
            lifetime=lifetime,
            call_method=call_method,
            local=local,
            *args,
            **kwargs,
        )

    # Caching Methods
    def unlimited_cache(self, *args: Any, **kwargs: Any) -> Any:
        """Caching with no limit on items in the cache.

        Args:
            *args: Arguments of the wrapped function.
            **kwargs: Keyword Arguments of the wrapped function.

        Returns:
            The result of the wrapped function.
        """
        key = self.create_key(args, kwargs, self.typed)
        cache_item = self.cache_container.get(key, search_sentinel)

        if cache_item is not search_sentinel:
            return cache_item.result
        else:
            result = self.__func__(*args, **kwargs)
            self.cache_container[key] = self.cache_item_type(key=key, result=result)
            return result

    def limited_cache(self, *args: Any, **kwargs: Any) -> Any:
        """Caching that does not cache new results when cache is full.

        Args:
            *args: Arguments of the wrapped function.
            **kwargs: Keyword Arguments of the wrapped function.

        Returns:
            The result of the wrapped function.
        """
        key = self.create_key(args, kwargs, self.typed)
        cache_item = self.cache_container.get(key, search_sentinel)

        if cache_item is not search_sentinel:
            return cache_item.result
        else:
            result = self.__func__(*args, **kwargs)
            if self.cache_container.__len__() <= self._maxsize:
                self.cache_container[key] = self.cache_item_type(result=result)
            return result

    # Cache Control
    def clear_cache(self) -> None:
        """Clear the cache and update the expiration of the cache."""
        self.cache_container.clear()
        self.priority.clear()
        if self.lifetime is not None:
            self.expiration = perf_counter() + self.lifetime

    def set_maxsize(self, value: int) -> None:
        """Change the cache's max size to a new value and updates the cache to its optimal handle function.

        Args:
            value: The new max size of the cache.
        """
        if value is None:
            self.cache_method = "unlimited_cache"
        elif value == 0:
            self.cache_method = "no_cache"
        else:
            self.cache_method = "limited_cache"

        self._maxsize = value

    def poll(self) -> bool:
        """Check if the cache has reached its max size."""
        return self.cache_container.__len__() <= self._maxsize

    def get_length(self) -> int:
        """Gets the length of the cache."""
        return self.cache_container.__len__()


class TimedCacheMethod(TimedCacheCallable, BaseTimedCacheMethod):
    """A method class for TimedCache."""


class TimedCache(TimedCacheCallable, BaseTimedCache):
    """A function class for TimedCache."""

    # Attributes #
    method_type: type[BaseTimedCacheMethod] = TimedCacheMethod

    # Instance Methods #
    # Binding
    def bind(self, instance: Any = None, owner: type[Any] | None = None) -> TimedCacheMethod:
        """Creates a method of this function which is bound to another object.

        Args:
            instance: The object to bind the method to.
            owner: The class of the object being bound to.

        Returns:
            The bound method of this function.
        """
        return self.method_type(
            func=self,
            instance=instance,
            owner=owner,
            typed=self.typed,
            lifetime=self.lifetime,
            call_method=self.call_method,
            local=self.is_local,
            maxsize=self.maxsize,
        )

    def bind_to_attribute(
        self,
        instance: Any = None,
        owner: type[Any] | None = None,
        name: str | None = None,
    ) -> TimedCacheMethod:
        """Creates a method of this function which is bound to another object and sets the method an attribute.

        Args:
            instance: The object to bind the method to.
            owner: The class of the object being bound to.
            name: The name of the attribute to set the method to. Default is the function name.

        Returns:
            The bound method of this function.
        """
        if name is None:
            name = self.__func__.__name__

        method = self.method_type(
            func=self,
            instance=instance,
            owner=owner,
            typed=self.typed,
            lifetime=self.lifetime,
            call_method=self.call_method,
            local=self.is_local,
            maxsize=self.maxsize,
        )
        setattr(instance, name, method)

        return method


# Functions #
def timed_cache(
    maxsize: int | None = None,
    typed: bool = False,
    lifetime: int | float | None = None,
    call_method: str | None = None,
    local: bool = True,
) -> Callable[[AnyCallable], TimedCache]:
    """A factory to be used a decorator that sets the parameters of timed cache function factory.

    Args:
        maxsize: The max size of the cache.
        typed: Determines if the function's arguments are type sensitive for caching.
        lifetime: The period between cache resets in seconds.
        call_method: The default call method to use.
        local: Determines if the cache is local for all method bindings or for each instance.

    Returns:
        The parameterized timed cache function factory.
    """

    def timed_cache_factory(func: AnyCallable) -> TimedCache:
        """A factory for wrapping a function with a TimedCache object.

        Args:
            func: The function to wrap with a TimedCache.

        Returns:
            The TimeCache object which wraps the given function.
        """
        return TimedCache(
            func,
            maxsize=maxsize,
            typed=typed,
            lifetime=lifetime,
            call_method=call_method,
            local=local,
        )

    return timed_cache_factory
