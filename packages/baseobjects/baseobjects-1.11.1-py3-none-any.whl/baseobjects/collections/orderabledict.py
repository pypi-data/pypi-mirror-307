"""orderabledict.py
A dictionary with an adjustable order and additional supporting methods.
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
from collections.abc import Mapping, Iterable, Iterator
from typing import Any

# Third-Party Packages #

# Local Packages #
from ..bases import BaseDict
from ..typing import KeyType, ValueType


# Definitions #
# Static #
SENTINEL = object()


# Classes #
class OrderableDict(BaseDict):
    """A dictionary with an adjustable order and additional supporting methods.

    Attributes:
        order: The order of this dictionary.

    Args:
        dict_: An object to build this dictionary from
        *args: Arguments for creating a dictionary.
        **kwargs: Keyword arguments for creating a dictionary.
    """

    # Attributes #
    order: list[KeyType, ...]

    # Magic Methods #
    # Construction/Destruction
    def __init__(self, dict_: Any = None, /, *args: Any, **kwargs: Any) -> None:
        # New Attributes #
        self.order: list[KeyType, ...] = []

        # Parent Attributes #
        super().__init__(dict_, *args, **kwargs)

    # Container Methods
    def __setitem__(self, key: KeyType, value: ValueType) -> None:
        """Sets an item in this object."""
        if key not in self.data:
            self.order.append(key)
        self.data[key] = value

    def __delitem__(self, key: KeyType) -> None:
        """Deletes an item from this object."""
        del self.data[key]
        self.order.remove(key)

    def __iter__(self) -> Iterator[KeyType]:
        """Returns an iterator for the keys."""
        return iter(self.order)

    # Instance Methods #
    def get_index(self, index: int, default: Any = SENTINEL) -> ValueType:
        """Gets a value base on its key's index in the order.

        Args:
            index: The index of the key to get.
            default: The value to return if the index is outside the range.

        Returns:
            The requested value.
        """
        try:
            return self.data.get(self.order[index])
        except IndexError as e:
            if default is not SENTINEL:
                return default
            else:
                raise e

    def set_index(self, index: int, value: ValueType) -> None:
        """Sets a key's value based on its index in the order.

        Args:
            index: The index of the key to set.
            value: The value to set at the key
        """
        self.data[self.order[index]] = value

    def setdefault(self, key: KeyType, default: ValueType = None) -> ValueType:
        """Gets a value with a key but adds the key and a default value to this dictionary if it was not present.

        Args:
            key: The key to get or add if it was not in the dictionary.
            default: The value to add to the dictionary if not present.
        """
        if key not in self.data:
            self.order.append(key)
        return self.data.setdefault(key, default)

    def insert(self, index: int, key: KeyType, value: ValueType) -> None:
        """Adds a key and value and inserts it into order or raises an error the key if it already exists.

        Args:
            index: The index to insert into the order.
            key: The key of value to insert.
            value: The value to set at the key.
        """
        if key in self.data:
            raise KeyError("Key already exists.")

        self.order.insert(index, key)
        self.data[key] = value

    def insert_move(self, index: int, key: KeyType, value: ValueType) -> None:
        """Adds a key and value and inserts it into order or moves the key if it already exists.

        Args:
            index: The index to insert into the order.
            key: The key of value to insert.
            value: The value to set at the key.
        """
        if key in self.data:
            old = self.order.index(key)
            if index < old:
                self.order.insert(index, value)
                self.order.remove(old + 1)
            elif index > old + 1:
                self.order.insert(index, value)
                self.order.remove(old)
        else:
            self.order.insert(index, key)

        self.data[key] = value

    def append(self, key: KeyType, value: ValueType) -> None:
        """Adds a key and value to this dictionary and appends it to the order if it was not present.

        Args:
            key: The key to add to the dictionary.
            value: The value to add to the dictionary
        """
        self[key] = value

    def update(self, m: Mapping | Iterable[tuple[KeyType, ValueType]] | None = None, **kwargs: ValueType) -> None:
        """Updates the keys and values of this dictionary, any new keys are appended to the order.

        Args:
            m: An object with the keys and values to add.
            **kwargs: The new values to add with the names as the keys.
        """
        for key, value in ({} if m is None else dict(m) | kwargs).items():
            self[key] = value

    def pop(self, key: KeyType) -> ValueType:
        """Pops a value from the key in this orderable dictionary.

        Args:
            key: The key of the value to pop.

        Returns:
            The requested value.
        """
        self.order.remove(key)
        return self.data.pop(key)

    def pop_index(self, index: int = -1) -> ValueType:
        """Pops the value at the index in this orderable dictionary.

        Args:
            index: The index of the value to pop.

        Returns:
            The value requested.
        """
        return self.data.pop(self.order.pop(index))

    def popitem(self) -> tuple[KeyType, ValueType]:
        """Pops the last key and its value.

        Returns:
            The key and value.
        """
        key = self.order.pop()
        return (key, self.data.pop(key))

    def remove(self, key: KeyType) -> None:
        """Removes a key from this dictionary."""
        del self[key]

    def clear(self) -> None:
        """Removes all items from this orderable dictionary."""
        self.data.clear()
        self.order.clear()

    def reverse(self) -> None:
        """Reverses the order of this dictionary."""
        self.order.reverse()
