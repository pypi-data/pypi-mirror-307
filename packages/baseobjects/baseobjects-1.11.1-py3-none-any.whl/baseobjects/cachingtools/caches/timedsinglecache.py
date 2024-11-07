"""timedsinglecache.py
A timed cache that only hold a single item.
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
from collections.abc import Callable, Hashable
from time import perf_counter
from typing import Any

# Third-Party Packages #

# Local Packages #
from ...typing import AnyCallable
from .basetimedcache import BaseTimedCacheCallable, BaseTimedCacheMethod, BaseTimedCache


# Definitions #
# Classes #
class TimedSingleCacheCallable(BaseTimedCacheCallable):
    """A periodically clearing single item cache wrapper object for a function.

    Attributes:
        args_key: The generated argument key of the current cached result.
    """

    # Attributes #
    _cache_method: str = "caching"
    args_key: Hashable | None = None

    # Instance Methods #
    # Caching Methods
    def caching(self, *args: Any, **kwargs: Any) -> Any:
        """Caching with no limit on items in the cache.

        Args:
            *args: Arguments of the wrapped function.
            **kwargs: Keyword Arguments of the wrapped function.

        Returns:
            The result of the wrapped function.
        """
        key = self.create_key(args, kwargs, self.typed)
        if key != self.args_key:
            self.cache_container = self.__func__(*args, **kwargs)
            self.args_key = key

        return self.cache_container

    # Cache Control
    def refresh_expiration(self) -> None:
        """Refreshes the expiration to be a lifetime later than now."""
        if self.lifetime is not None:
            self.expiration = perf_counter() + self.lifetime

    def clear_cache(self) -> None:
        """Clears the cache and update the expiration of the cache."""
        self.cache_container = None
        self.args_key = None
        if self.lifetime is not None:
            self.expiration = perf_counter() + self.lifetime


class TimedSingleCacheMethod(TimedSingleCacheCallable, BaseTimedCacheMethod):
    """A method class for TimedSingleCache."""


class TimedSingleCache(TimedSingleCacheCallable, BaseTimedCache):
    """A function class for TimedSingleCache."""

    # Attributes #
    method_type: type[BaseTimedCacheMethod] = TimedSingleCacheMethod


# Functions #
def timed_single_cache(
    typed: bool = False,
    lifetime: int | float | None = None,
    call_method: str | None = None,
    local: bool = True,
) -> Callable[[AnyCallable], TimedSingleCache]:
    """A factory to be used a decorator that sets the parameters of timed single cache function factory.

    Args:
        typed: Determines if the function's arguments are type sensitive for caching.
        lifetime: The period between cache resets in seconds.
        call_method: The default call method to use.
        local: Determines if the cache is local for all method bindings or for each instance.

    Returns:
        The parameterized timed single cache function factory.
    """

    def timed_single_cache_factory(func: AnyCallable) -> TimedSingleCache:
        """A factory for wrapping a function with a TimedSingleCache object.

        Args:
            func: The function to wrap with a TimedSingleCache.

        Returns:
            The TimeSingleCache object which wraps the given function.
        """
        return TimedSingleCache(
            func,
            typed=typed,
            lifetime=lifetime,
            call_method=call_method,
            local=local,
        )

    return timed_single_cache_factory
