"""timedkeylesscache.py
A timed cache that only hold a single item and does not create a key from arguments.
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
from .timedsinglecache import TimedSingleCacheCallable, TimedSingleCacheMethod, TimedSingleCache


# Definitions #
# Classes #
class TimedKeylessCacheCallable(TimedSingleCacheCallable):
    """A periodically clearing cache wrapper object for a function that only has one result.

    Attributes:
        args_key: The generated argument key of the current cached result.
    """

    # Attributes #
    args_key: bool | None = None

    # Instance Methods #
    # Caching
    def caching(self, *args: Any, **kwargs: Any) -> Any:
        """Caching with no limit on items in the cache.

        Args:
            *args: Arguments of the wrapped function.
            **kwargs: Keyword Arguments of the wrapped function.

        Returns:
            The result of the wrapped function.
        """
        if not self.args_key:
            self.cache_container = self.__wrapped__(*args, **kwargs)
            self.args_key = True

        return self.cache_container


class TimedKeylessCacheMethod(TimedKeylessCacheCallable, TimedSingleCacheMethod):
    """A method class for TimedKeylessCache."""


class TimedKeylessCache(TimedKeylessCacheCallable, TimedSingleCache):
    """A function class for TimedKeylessCache."""

    # Attributes #
    method_type: type[TimedSingleCacheMethod] = TimedKeylessCacheMethod
    _bind_method: str = "bind_to_attribute"


# Functions #
def timed_keyless_cache(
    typed: bool = False,
    lifetime: int | float | None = None,
    call_method: str | None = None,
    local: bool = True,
) -> Callable[[AnyCallable], TimedKeylessCache]:
    """A factory to be used a decorator that sets the parameters of timed keyless cache function factory.

    Args:
        typed: Determines if the function's arguments are type sensitive for caching.
        lifetime: The period between cache resets in seconds.
        call_method: The default call method to use.
        local: Determines if the cache is local for all method bindings or for each instance.

    Returns:
        The parameterized timed keyless cache function factory.
    """

    def timed_keyless_cache_factory(func: AnyCallable) -> TimedKeylessCache:
        """A factory for wrapping a function with a TimedKeylessCache object.

        Args:
            func: The function to wrap with a TimedKeylessCache.

        Returns:
            The TimeKeylessCache object which wraps the given function.
        """
        return TimedKeylessCache(
            func,
            typed=typed,
            lifetime=lifetime,
            call_method=call_method,
            local=local,
        )

    return timed_keyless_cache_factory
