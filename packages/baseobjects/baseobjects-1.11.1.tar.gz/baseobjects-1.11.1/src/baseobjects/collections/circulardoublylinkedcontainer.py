"""circulardoublylinkedcontainer.py
A circular doubly linked container which is a fast and efficient way to store ordered data, especially if constantly
changes size.
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
import copy
from typing import Any, Optional
import weakref

# Third-Party Packages #

# Local Packages #
from ..bases import BaseObject
from ..functions import singlekwargdispatch


# Definitions #
# Classes #
class LinkedNode(BaseObject):
    """A node in a circular doubly linked container.

    Attributes:
        _previous: A weak reference to the previous node.
        _next: A weak reference to the next node.
        data: The data contained within this node.

    Args:
        data: The data to contain within this node.
        previous: The previous node.
        next_: The next node.
    """

    # Attributes #
    _previous: weakref.ReferenceType
    _next: weakref.ReferenceType

    data: Any | None = None

    # Properties #
    @property
    def previous(self) -> Any:
        """The previous node."""
        try:
            return self._previous()
        except TypeError:
            return None

    @previous.setter
    def previous(self, value: Any) -> None:
        self._previous = None if value is None else weakref.ref(value)

    @property
    def next(self) -> Any:
        """The next node."""
        try:
            return self._next()
        except TypeError:
            return None

    @next.setter
    def next(self, value: Any) -> None:
        self._next = None if value is None else weakref.ref(value)

    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        data: Any | None = None,
        previous: Optional["LinkedNode"] = None,
        next_: Optional["LinkedNode"] = None,
        *args: Any,
        init: bool = True,
        **kwargs: Any,
    ) -> None:
        # New Attributes #
        self._previous: weakref.ReferenceType = weakref.ref(self)
        self._next: weakref.ReferenceType = weakref.ref(self)

        # Parent Attributes #
        super().__init__(*args, init=False, **kwargs)

        # Object Construction #
        if init:
            self.construct(data=data, previous=previous, next_=next_)

    # Instance Methods #
    # Constructors
    def construct(
        self,
        data: Any | None = None,
        previous: Optional["LinkedNode"] = None,
        next_: Optional["LinkedNode"] = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Constructs this object.

        Args:
            data: The data to contain within this node.
            previous: The previous node.
            next_: The next node.
        """
        if previous is not None:
            self.previous = weakref.ref(previous)

        if next_ is not None:
            self.next = weakref.ref(next_)

        self.data = data

        super().construct(*args, **kwargs)


class CircularDoublyLinkedContainer(BaseObject):
    """A container that uses nodes which are doubly linked to one another to store data.

    Attributes:
        first_node: The first linked node in this container.
        nodes: The set of nodes in this container.
    """

    # Attributes #
    first_node: LinkedNode | None = None
    nodes: set[LinkedNode] = set()

    # Properties #
    @property
    def is_empty(self) -> bool:
        """Determines if this container is empty."""
        return self.first_node is None

    @property
    def last_node(self) -> LinkedNode:
        """The last node in this container."""
        return self.first_node.previous

    # Magic Methods #
    # Construction/Destruction
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        # Parent Attributes #
        super().__init__(*args, **kwargs)

        # Attributes #
        self.nodes: set[LinkedNode] = set()

    def __deepcopy__(self, memo: dict | None = None, _nil=[]) -> "CircularDoublyLinkedContainer":
        """Creates a deep copy of this object.

        Args:
            memo: A dictionary of user defined information to pass to another deepcopy call which it will handle.

        Returns:
            A deep copy of this object.
        """
        new_obj = type(self)()
        if not self.is_empty:
            original_node = self.first_node
            new_obj.append(data=copy.deepcopy(original_node.data))
            while original_node.next is not self.first_node:
                new_obj.append(data=copy.deepcopy(original_node.data))
                original_node = original_node.next

        return new_obj

    # Container Methods
    def __len__(self) -> int:
        """Gets this object's length (number of nodes).

        Returns:
            The number of nodes in this object.
        """
        return self.get_length()

    def __getitem__(self, item: int) -> LinkedNode:
        """The method that allows index retrievals a node.

        Args:
            item: The index of the item to get.

        Returns:
            The node based on the index.
        """
        return self.get_item(item)

    def __iter__(self) -> Iterable:
        """Returns an iterable representation of this object.

        Returns:
            The iterable representation of this of object.
        """
        return self.forward_iter()

    # Bitwise Operators
    def __lshift__(self, other: int) -> None:
        """Shifts the start of nodes to the left by an amount.

        Args:
            other: The number of nodes to shift to the left.
        """
        self.shift_left(other)

    def __rshift__(self, other: int) -> None:
        """Shifts the start of nodes to the right by an amount.

        Args:
            other: The number of nodes to right to the left.
        """
        self.shift_right(other)

    # Instance Methods #
    # Container Methods
    def get_length(self) -> int:
        """Gets the number of nodes in this container.

        Returns:
            The number of nodes in this object.
        """
        len(self.nodes)

    def get_item(self, index: int) -> LinkedNode:
        """Gets a node based on its index from the start node.

        Args:
            index: The index of the item to get.

        Returns:
            The node based on the index.
        """
        node = self.first_node

        # Forward Indexing
        if index > 0:
            for i in range(index):
                node = node.next()
        # Reverse Indexing
        elif index < 0:
            index *= -1
            for i in range(index):
                node = node.previous()

        return node

    @singlekwargdispatch("data")
    def append(self, data: Any) -> LinkedNode:
        """Add a new node and data to the end of the container.

        Args:
            data: The data to add to the new last node.

        Returns:
            The LinkedNode added to the container.
        """
        new_node = LinkedNode(data)
        self.nodes.add(new_node)
        weak_node = weakref.ref(new_node)

        if self.first_node is None:
            self.first_node = new_node
        else:
            self.last_node.next = weak_node
            self.first_node.previous = weak_node

        return new_node

    @append.register
    def _(self, data: LinkedNode) -> LinkedNode:
        """Add a new node and data to the end of the container.

        Args:
            data: The data to add to the new last node.

        Returns:
            The LinkedNode added to the container.
        """
        self.nodes.add(data)
        weak_node = weakref.ref(data)

        if self.first_node is None:
            self.first_node = data
        else:
            self.last_node.next = weak_node
            self.first_node.previous = weak_node

        return data

    @singlekwargdispatch("data")
    def insert(self, data: Any, index: int) -> LinkedNode:
        """Add a new node and data at index within the container.

        Args:
            data: The data to add to the new node.
            index: The place to insert the new node at.

        Returns
            The LinkedNode added to the container.
        """
        new_node = LinkedNode(data)
        self.nodes.add(new_node)

        if self.first_node is None:
            self.first_node = new_node
        else:
            point = self.get_item(index=index)
            new_node.next = point
            new_node.previous = point.previous
            new_node.previous.next = new_node
            point.previous = new_node

        return new_node

    @insert.register
    def _(self, data: LinkedNode, index: int) -> LinkedNode:
        """Add a new node and data at index within the container.

        Args:
            data: The data to add to the new node.
            index: The place to insert the new node at.

        Returns
            The LinkedNode added to the container.
        """
        self.nodes.add(data)

        if self.first_node is None:
            self.first_node = data
        else:
            point = self.get_item(index=index)
            data.next = point
            data.previous = point.previous
            data.previous.next = data
            point.previous = data

        return data

    def remove_node(self, node: LinkedNode) -> None:
        """Removes a node from the container.

        Args:
            node: The node to move.
        """
        node.next.previous = node.previous
        node.previous.next = node.next
        self.nodes.remove(node)

    def pop(self, index: int = -1) -> LinkedNode:
        """Removes a node at the index within the container and return it.

        Args:
            index: The index of the node to pop.

        Returns
            The LinkedNode removed from the container.
        """
        node = self.get_item(index=index)
        self.remove_node(node)
        return node

    def clear(self) -> None:
        """Clears this container by removing the first node."""
        self.nodes.clear()
        self.first_node = None

    # Node Manipulation
    def move_node_start(self, node: LinkedNode) -> None:
        """Move a node to the start of the container.

        Args:
            node: The node to move.
        """
        self.move_node_end(node)
        self.first_node = node

    def move_node_end(self, node: LinkedNode) -> None:
        """Move a node to the end of container.

        Args:
            node: The node to move.
        """
        node.next.previous = node.previous
        node.previous.next = node.next
        node.next = self.first_node
        node.previous = self.last_node
        self.last_node.next = node
        self.first_node.previous = node

    def move_node(self, node: LinkedNode, index: int) -> None:
        """Move a node to an index within the container.

        Args:
            node: The node to move.
            index: The place to move the node to.
        """
        node.next.previous = node.previous
        node.previous.next = node.next
        point = self.get_item(index=index)
        node.next = point
        node.previous = point.previous
        node.previous.next = node
        point.previous = node

    def shift_left(self, value: int = 1) -> None:
        """Shift the start of nodes to the left by an amount.

        Args:
            value: The number of nodes to shift to the left.
        """
        if value == 1:
            self.first_node = self.first_node.next
        elif value > 1:
            i = 0
            while i <= value:
                self.first_node = self.first_node.next
                i += 1

    def shift_right(self, value: int = 1) -> None:
        """Shift the start of nodes to the right by an amount.

        Args:
            value: The number of nodes to right to the left.
        """
        if value == 1:
            self.first_node = self.first_node.previous
        elif value > 1:
            i = 0
            while i <= value:
                self.first_node = self.first_node.previous
                i += 1

    # Iteration
    def forward_iter(self) -> Iterable:
        """Creates an iterable which iterates through the nodes from first to last.

        Returns:
            The forward iterable.
        """
        node = yield self.first_node
        node = node.next
        while node is not self.first_node:
            yield node
            node = node.next

    def reverse_iter(self) -> Iterable:
        """Creates an iterable which iterates through the nodes from last to first.

        Returns:
            The reverse iterable.
        """
        node = yield self.last_node
        node = node.previous
        while node is not self.last_node:
            yield node
            node = node.previous

    def forward_cycle(self) -> Iterable:
        """Creates an iterable which cycles through the nodes from first to last.

        Returns:
            The forward cycle.
        """
        node = yield self.first_node
        while True:
            node = yield node.next

    def reverse_cycle(self) -> Iterable:
        """Creates an iterable which cycles through the nodes from last to first.

        Returns:
            The reverse cycle.
        """
        node = yield self.last_node
        while True:
            node = yield node.previous
