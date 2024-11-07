"""groupedlist.py
A list which contains any item, but nested GroupLists' contents are treated as if they are elements of this list.
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
from collections import deque
from collections.abc import Iterable, Iterator
from typing import Any, Union, Optional

# Third-Party Packages #
import bidict

# Local Packages #
from ..bases import BaseList, search_sentinel


# Definitions #
# Classes #
class GroupedList(BaseList):
    """A list which contains any item, but nested GroupLists' contents are treated as if they are elements of this list.

    Attributes:
        parents: The parent and the ancestor GroupLists which this GroupList was created from.
        groups: The named GroupLists within this GroupList.

    Args:
        items: The items to add to this GroupList.
        parent: The parent GroupList of this GroupList.
        parents: The parent and ancestors of this GroupList
        init: Determines if this object will construct.
    """

    # Attributes #
    # New Attributes #
    parents: set["GroupedList"]
    groups: bidict.bidict

    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        items: Iterable[Any] | None = None,
        parent: Optional["GroupedList"] = None,
        parents: Iterable["GroupedList"] | None = None,
        init: bool = True,
    ) -> None:
        # New Attributes #
        self.parents = set()
        self.groups = bidict.bidict()

        # Parent Attributes #
        super().__init__()

        # Object Construction #
        if init:
            self.construct(items=items, parent=parent, parents=parents)

    def __copy__(self) -> "GroupedList":
        new = self.__class__(items=self.data, parents=self.parents)
        self.add_parent_to_children(new)
        new.groups.update(self.groups)
        return new

    # Container Methods
    def __len__(self) -> int:
        return self.get_length()

    def __getitem__(self, i: int | str | slice) -> Any | list[Any]:
        if isinstance(i, slice):
            return self.get_slice(i)
        elif isinstance(i, str):
            return self.groups[i]
        else:
            return self.get_item(i)

    def __setitem__(self, i, item) -> None:
        self.set_item(i, item)

    def __delitem__(self, i) -> None:
        self.delete_item(i)

    def __iter__(self) -> Iterator[Any]:
        for item in self.data:
            if isinstance(item, GroupedList) and self.check_if_child(item):
                for sub_item in item:
                    yield sub_item
            else:
                yield item

    def __contains__(self, item: Any) -> bool:
        return item in self.as_flat_list()

    # Representation
    def __repr__(self) -> str:
        return repr(self.as_flat_tuple())

    def __hash__(self) -> int:
        """Overrides hash to make the class hashable.

        Returns:
            The system ID of the class.
        """
        return id(self)

    # Type Conversion
    def __cast(self, other: Any) -> Any:
        return other.as_flat_list() if isinstance(other, GroupedList) else other

    # Comparison
    def __lt__(self, other: Any) -> bool:
        return self.as_flat_list() < self.__cast(other)

    def __le__(self, other: Any) -> bool:
        return self.as_flat_list() <= self.__cast(other)

    def __eq__(self, other: Any) -> bool:
        return self.as_flat_list() == self.__cast(other)

    def __gt__(self, other: Any) -> bool:
        return self.as_flat_list() > self.__cast(other)

    def __ge__(self, other: Any) -> bool:
        return self.as_flat_list() >= self.__cast(other)

    # Arithmetic
    def __add__(self, other: Any) -> "GroupedList":
        return self.add(other)

    def __radd__(self, other: Any) -> "GroupedList":
        return self.radd(other)

    def __iadd__(self, other: Any) -> "GroupedList":
        return self.iadd(other)

    def __mul__(self, n: int) -> "GroupedList":
        new = self.__class__(items=self.data * n, parents=self.parents)
        self.add_parent_to_children(new)
        new.groups.update(self.groups)
        return new

    __rmul__ = __mul__

    def __imul__(self, n: int) -> "GroupedList":
        self.data *= n
        return self

    # Instance Methods #
    # Constructors/Destructors
    def construct(
        self,
        items: Iterable[Any] | None = None,
        parent: Optional["GroupedList"] = None,
        parents: Iterable["GroupedList"] | None = None,
    ) -> None:
        """Constructs this object.

        Args:
            items: The items to add to this GroupList.
            parent: The parent GroupList of this GroupList.
            parents: The parent and ancestors of this GroupList
        """
        if parent is not None:
            self.parents.add(parent)

        if parents is not None:
            self.parents.update(parents)

        if items is not None:
            self.data.clear()
            self.data.extend(items)

    def check_if_child(self, other: "GroupedList") -> bool:
        return self in other.parents

    def check_if_parent(self, other: "GroupedList") -> bool:
        return other in self.parents

    def add_parent_to_children(self, other: "GroupedList") -> None:
        for item in self.data:
            if isinstance(item, GroupedList) and self.check_if_child(item):
                item.parents.add(other)

    def remove_parent_from_children(self, other: "GroupedList") -> None:
        for item in self.data:
            if isinstance(item, GroupedList) and self.check_if_child(item):
                item.parents.remove(other)

    def get_group_lengths(self, recurse: bool = False) -> tuple[int, tuple]:
        lengths = deque()
        for item in self.data:
            if isinstance(item, GroupedList) and self.check_if_child(item):
                if recurse:
                    lengths.append(item.get_group_lengths(recurse))
                else:
                    lengths.append(len(item))

        return (len(self.data) - len(self.groups), tuple(lengths))

    def get_length(self) -> int:
        n_items = len(self.data) - len(self.groups)
        for group in self.groups.values():
            n_items += len(group)
        return n_items

    def create_group(self, name: str, items: Iterable | None = None) -> "GroupedList":
        if name not in self.groups:
            new_group = self.__class__(items=items, parent=self)
            self.groups[name] = new_group
            self.data.append(new_group)
            return new_group
        else:
            raise KeyError(f"{name} group already exists.")

    def require_group(self, name: str | Iterable[str]) -> "GroupedList":
        if isinstance(name, str):
            names = [name]
        else:
            names = list(name)

        # Require name at this level
        first = names.pop()
        new_group = self.groups.get(first, search_sentinel)
        if new_group is search_sentinel:
            new_group = self.__class__(parent=self)
            self.groups[first] = new_group
            self.data.append(new_group)

        # Recurse if needed
        if names:
            new_group = new_group.require_group(names)

        return new_group

    def remove_group(self, group: Union[str, "GroupedList"]) -> None:
        if isinstance(group, str):
            name = group
            group = self.groups[name]
        else:
            name = self.groups.inverse[group]

        self.data.remove(group)
        group.parents.remove(self)
        del self.groups[name]

    def get_group(self, name: str | Iterable[str]) -> "GroupedList":
        if isinstance(name, str):
            names = [name]
        else:
            names = list(name)

        # Get name at this level
        first = names.pop()
        new_group = self.groups[first]

        # Recurse if needed
        if names:
            new_group = new_group.get_group(names)

        return new_group

    def add_group(self, group: "GroupedList", name: str) -> None:
        self.data.append(group)
        self.groups[name] = group

    def get_item(self, i, group: str | None = None) -> Any:
        if group is not None:
            return self.groups[group].get_item(i)
        elif i < 0:
            data = reversed(self.data)
            i = -i - 1
            reverse = True
        else:
            data = self.data
            reverse = False

        for item in data:
            if i <= 0:
                if isinstance(item, GroupedList) and self.check_if_child(item):
                    i = -i - 1 if reverse else i
                    return item.get_item(i)
                else:
                    return item
            elif isinstance(item, GroupedList) and self.check_if_child(item):
                n_items = len(item)
                if i < n_items:
                    i = -i - 1 if reverse else i
                    return item.get_item(i)
                else:
                    i -= n_items
            else:
                i -= 1

        raise IndexError("index out of range")

    def get_slice(self, slice_: slice, group: str | None = None):
        if group is not None:
            return self.groups[group].get_slice(slice_)
        else:
            return self.as_flat_list()[slice_]

    def set_item(self, i, value, group: str | None = None) -> None:
        if group is not None:
            return self.groups[group].set_item(i, value)
        elif i < 0:
            self.data.reverse()
            i = -i - 1
            reverse = True
        else:
            reverse = False

        for j, item in enumerate(self.data):
            if i <= 0:
                if isinstance(item, GroupedList) and self.check_if_child(item):
                    i = -i - 1 if reverse else i
                    item.set_item(i, value)
                else:
                    self.data[j] = value

                if reverse:
                    self.data.reverse()

                return
            elif isinstance(item, GroupedList) and self.check_if_child(item):
                n_items = len(item)
                if i < n_items:
                    i = -i - 1 if reverse else i
                    item.set_item(i, value)
                    if reverse:
                        self.data.reverse()
                    return
                else:
                    i -= n_items
            else:
                i -= 1

        raise IndexError("index out of range")

    def delete_item(self, i, group: str | None = None) -> None:
        if group is not None:
            return self.groups[group].delete_item(i)
        elif i < 0:
            self.data.reverse()
            i = -i - 1
            reverse = True
        else:
            reverse = False

        for j, item in enumerate(self.data):
            if i <= 0:
                if isinstance(item, GroupedList) and self.check_if_child(item):
                    i = -i - 1 if reverse else i
                    item.delete_item(i)
                else:
                    del self.data[j]

                if reverse:
                    self.data.reverse()

                return
            elif isinstance(item, GroupedList) and self.check_if_child(item):
                n_items = len(item)
                if i < n_items:
                    i = -i - 1 if reverse else i
                    item.delete_item(i)
                    if reverse:
                        self.data.reverse()
                    return
                else:
                    i -= n_items
            else:
                i -= 1

        raise IndexError("index out of range")

    def append(self, item: Any, group: str | None = None) -> None:
        if group is None:
            self.data.append(item)
        else:
            group = self.require_group(name=group)
            group.append(item)

    def insert(self, i, item, group: str | None = None):
        if group is None:
            return self.data.insert(i, item)
        elif i < 0:
            self.data.reverse()
            i = -i - 1
            reverse = True
        else:
            reverse = False

        for j, contained_item in enumerate(self.data):
            if i <= 0:
                if isinstance(contained_item, GroupedList) and self.check_if_child(contained_item):
                    i = -i - 1 if reverse else i
                    contained_item.set_item(i, item)
                else:
                    index = -j - 1 if reverse else j
                    self.data.insert(index, item)

                if reverse:
                    self.data.reverse()

                return
            elif isinstance(contained_item, GroupedList) and self.check_if_child(contained_item):
                n_items = len(contained_item)
                if i < n_items:
                    i = -i - 1 if reverse else i
                    contained_item.insert(i, item)
                    if reverse:
                        self.data.reverse()
                    return
                else:
                    i -= n_items
            else:
                i -= 1

        self.data.append(item)
        if reverse:
            self.data.reverse()

    def pop(self, i=-1, group: str | None = None):
        if group is not None:
            return self.groups[group].delete_item(i)
        elif i < 0:
            self.data.reverse()
            i = -i - 1
            reverse = True
        else:
            reverse = False

        for j, item in enumerate(self.data):
            if i <= 0:
                if isinstance(item, GroupedList) and self.check_if_child(item):
                    i = -i - 1 if reverse else i
                    result = item.pop(i)
                else:
                    index = -j - 1 if reverse else j
                    result = self.data[index]
                    del self.data[index]

                if reverse:
                    self.data.reverse()

                return result
            elif isinstance(item, GroupedList) and self.check_if_child(item):
                n_items = len(item)
                if i < n_items:
                    i = -i - 1 if reverse else i
                    if reverse:
                        self.data.reverse()
                    return item.pop(i)
                else:
                    i -= n_items
            else:
                i -= 1
        return self.data.pop(i)

    def remove(self, item: Any, group: str | None = None) -> None:
        if group is not None:
            return self.groups[group].remove(item)
        else:
            for contained_item in self.data:
                if contained_item is item:
                    self.data.remove(item)
                    return
                elif isinstance(contained_item, GroupedList) and self.check_if_child(contained_item):
                    if item in contained_item:
                        contained_item.remove(item)
                        return
        raise ValueError("item is not present in this object")

    def clear(self, group: str | None = None) -> None:
        if group is None:
            self.data.clear()
            self.groups.clear()
        else:
            self.groups[group].clear()

    def count(self, item) -> int:
        return self.as_flat_list().count(item)

    def index(self, item, *args) -> int:
        return self.as_flat_list().index(item, *args)

    def reverse(self) -> None:
        self.data.reverse()
        for item in self.data:
            if isinstance(item, GroupedList) and self.check_if_child(item):
                item.reverse()

    def sort(self, /, *args, **kwds) -> None:
        self.data.sort(*args, **kwds)

    def extend(self, other: Iterable[Any], group: str | None = None) -> None:
        if isinstance(other, GroupedList):
            other.add_parent_to_children(self)
            self.data.extend(other.data)
            self.groups.update(other.groups | self.groups)
        elif group is not None:
            self.groups[group].extend(other)
        else:
            self.data.extend(other)

    def add(self, other: Any) -> "GroupedList":
        if not isinstance(other, Iterable):
            other = list(other)
        new = self.copy()
        new.extend(other)
        return new

    def radd(self, other: Any) -> "GroupedList":
        if isinstance(other, GroupedList):
            new = other.copy()
        else:
            if not isinstance(other, Iterable):
                other = list(other)
            new = self.__class__(items=other)

        new.extend(self)
        return new

    def iadd(self, other) -> "GroupedList":
        if not isinstance(other, Iterable):
            other = list(other)
        self.extend(other)
        return self

    def as_flat_tuple(self) -> tuple[Any]:
        """Return the contents of this GroupList as a flat tuple.

        Returns:
            A tuple with the contents of this GroupList.
        """
        return tuple(iter(self))

    def as_flat_list(self) -> list[Any]:
        """Return the contents of this GroupList as a flat list.

        Returns:
            A list with the contents of this GroupList.
        """
        return list(iter(self))
