"""timedlrucache.py
A lru cache that periodically resets and include its instantiation decorator function.
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
from typing import Any

# Third-Party Packages #

# Local Packages #
from ...typing import AnyCallable
from ...bases import search_sentinel
from .timedcache import TimedCacheCallable, TimedCacheMethod, TimedCache


# Definitions #
# Classes #
class TimedLRUCache(TimedCacheCallable):
    """A periodically clearing Least Recently Used (LRU) cache wrapper object for a function."""

    # Instance Methods #
    # LRU Caching
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
            self.priority.move_node_start(cache_item.priority_link)
            return cache_item.result
        else:
            result = self.__func__(*args, **kwargs)
            self.cache_container[key] = item = self.cache_item_type(key=key, result=result)
            priority_link = self.priority.insert(item, 0)
            item.priority_link = priority_link
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
            self.priority.move_node_start(cache_item.priority_link)
            return cache_item.result
        else:
            result = self.__func__(*args, **kwargs)
            if self.cache_container.__len__() <= self._maxsize:
                self.cache_container[key] = item = self.cache_item_type(key=key, result=result)
                priority_link = self.priority.insert(item, 0)
                item.priority_link = priority_link
            else:
                priority_link = self.priority.last_node
                old_key = priority_link.key

                item = self.cache_item_type(key=key, result=result, priority_link=priority_link)
                priority_link.data = item

                del cache_item[old_key]
                self.cache_container[key] = item

                self.priority.shift_right()

            return result


class TimedLRUCacheMethod(TimedLRUCache, TimedCacheMethod):
    """A method class for TimeLRUCache."""


class TimedLRUCache(TimedLRUCache, TimedCache):
    """A function class for TimedLRUCache."""

    # Attributes #
    method_type: type[TimedLRUCacheMethod] = TimedLRUCacheMethod


# Functions #
def timed_lru_cache(
    maxsize: int | None = None,
    typed: bool = False,
    lifetime: int | float | None = None,
    call_method: str | None = None,
    local: bool = False,
) -> Callable[[AnyCallable], TimedLRUCache]:
    """A factory to be used a decorator that sets the parameters of timed lru cache function factory.

    Args:
        maxsize: The max size of the cache.
        typed: Determines if the function's arguments are type sensitive for caching.
        lifetime: The period between cache resets in seconds.
        call_method: The default call method to use.
        local: Determines if the cache is local for all method bindings or for each instance.

    Returns:
        The parameterized timed lru cache function factory.
    """

    def timed_lru_cache_factory(func: AnyCallable) -> TimedLRUCache:
        """A factory for wrapping a function with a TimedLRUCache object.

        Args:
            func: The function to wrap with a TimedLRUCache.

        Returns:
            The TimeLRUCache object which wraps the given function.
        """
        return TimedLRUCache(
            func,
            maxsize=maxsize,
            typed=typed,
            lifetime=lifetime,
            call_method=call_method,
            local=local,
        )

    return timed_lru_cache_factory
