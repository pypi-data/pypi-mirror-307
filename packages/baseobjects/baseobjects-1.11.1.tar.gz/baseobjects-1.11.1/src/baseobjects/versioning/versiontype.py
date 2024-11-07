"""versiontype.py
A dataclass like object that contains a string name and associated class for a version. See versions for examples of
implementation.
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
from typing import Any

# Third-Party Packages #

# Local Packages #
from ..bases import BaseObject


# Definitions #
# Classes #
class VersionType(BaseObject):
    """A dataclass like object that contains a string name and associated class for a version.

    Attributes:
        name: The string name of this object.
        class_: The class of the version.
        head_class: The head class of the version.

    Args:
        name: The string name of this object.
        class_ : The class of the version.
        init: Determines if this object will construct.
    """

    # New Attributes #
    name: str | None = None
    class_: type | None = None
    head_class: type | None = None

    # Construction/Destruction
    def __init__(
        self,
        name: str | None = None,
        class_: type | None = None,
        head_class: type | None = None,
        init: bool = True,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        # Parent Attributes #
        super().__init__(*args, init=False, **kwargs)

        # Object Construction #
        if init:
            self.construct(name=name, class_=class_, head_class=head_class)

    # Representation
    def __hash__(self) -> int:
        """Overrides hash to make the object hashable.

        Returns:
            The system ID of the object.
        """
        return id(self)

    # Type Conversion
    def __str__(self) -> str:
        """Returns the str representation of the version.

        Returns:
            str: A str with the version numbers in order.
        """
        return self.name

    # Comparison
    def __eq__(self, other: Any) -> bool:
        """Expands on equals comparison to include comparing the version number.

        Args:
            other: The object to compare to this object.

        Returns:
            True if the other object or version number is equivalent.
        """
        if isinstance(other, type(self)):
            return other.name == self.name
        if isinstance(other, str):
            return other == self.name
        else:
            return super().__eq__(other)

    def __ne__(self, other: Any) -> bool:
        """Expands on not equals comparison to include comparing the version number.

        Args:
            other: The object to compare to this object.

        Returns:
            bool: True if the other object or version number is not equivalent.
        """
        if isinstance(other, type(self)):
            return other.name != self.name
        if isinstance(other, str):
            return other != self.name
        else:
            return super().__ne__(other)

    # Methods
    def construct(self, name: str | None = None, class_: type | None = None, head_class: type | None = None) -> None:
        """Constructs the version type object based on inputs.

        Args:
            name: The string name of this object.
            class_: The class of the version.
            head_class: The head class of the version.
        """
        if name is not None:
            self.name = name
        if class_ is not None:
            self.class_ = class_
        if head_class is not None:
            self.head_class = head_class
