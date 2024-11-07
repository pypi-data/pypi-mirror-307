"""version.py
Version is an abstract class which versions of different types can be defined from.
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
from abc import abstractmethod
from typing import Any

# Third-Party Packages #

# Local Packages #
from ..bases import BaseObject
from .versiontype import VersionType


# Definitions #
# Classes #
class Version(BaseObject):
    """An abstract class for creating versions which dataclass like classes that stores and handles a versioning.

    Class Attributes:
        default_version_name: The name of the version.

    Attributes:
        version_type: The type of version object this object is.

    Args:
        version: An object to derive a version from.
        ver_name: The name of the version type being used.
        init: Determines if this object will construct.
        **kwargs: More keyword arguments for constructing this object
    """

    # Attributes #
    default_version_name: str = "default"
    version_type: VersionType | None = None

    # Class Methods
    @classmethod
    def cast(cls, other: Any, pass_: bool = False) -> Any:
        """A cast method that optionally returns the original object rather than raise an error

        Args:
            other: An object to convert to this type.
            pass_: True to return original object rather than raise an error.

        Returns:
            obj: The converted object of this type or the original object.
        """
        try:
            other = cls(other)
        except TypeError as e:
            if not pass_:
                raise e

        return other

    @classmethod
    def create_version_type(cls, name: str = None) -> VersionType:
        """Create the version type of this version class.

        Args:
            name: The which this type will referred to.

        Returns:
           The version type of this version.
        """
        if name is None:
            name = cls.default_version_name
        return VersionType(name, cls)

    # Matic Methods
    # Construction/Destruction
    def __init__(
        self,
        version: Any | None = None,
        ver_name: str | None = None,
        init: bool = True,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        # Parent Attributes #
        super().__init__(*args, init=False, **kwargs)

        # Object Construction #
        if init:
            self.construct(version=version, ver_name=ver_name, **kwargs)

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
            A str with the version numbers in order.
        """
        return self.str()

    # Comparison
    @abstractmethod
    def __eq__(self, other: Any) -> bool:
        """Expands on equals comparison to include comparing the version number.

        Args:
            other: The object to compare to this object.

        Returns:
            True if the other object or version number is equivalent.
        """
        return super().__eq__(other)

    @abstractmethod
    def __ne__(self, other: Any) -> bool:
        """Expands on not equals comparison to include comparing the version number.

        Args:
            other: The object to compare to this object.

        Returns:
            True if the other object or version number is not equivalent.
        """
        return super().__ne__(other)

    @abstractmethod
    def __lt__(self, other: Any) -> bool:
        """Creates the less than comparison for these objects which includes str, list, and tuple.

        Args:
            other: The object to compare to this object.

        Returns:
            True if this object is less than to the other objects' version number.

        Raises:
            TypeError: If 'other' is a type that cannot be compared to.
        """
        other = self.cast(other, pass_=True)

        if isinstance(other, Version):
            return self.tuple() < other.tuple()
        else:
            raise TypeError(f"'>' not supported between instances of '{str(self)}' and '{str(other)}'")

    @abstractmethod
    def __gt__(self, other: Any) -> bool:
        """Creates the greater than comparison for these objects which includes str, list, and tuple.

        Args:
            other: The object to compare to this object.

        Returns:
            True if this object is greater than to the other objects' version number.

        Raises:
            TypeError: If 'other' is a type that cannot be compared to.
        """
        other = self.cast(other, pass_=True)

        if isinstance(other, Version):
            return self.tuple() > other.tuple()
        else:
            raise TypeError(f"'>' not supported between instances of '{str(self)}' and '{str(other)}'")

    @abstractmethod
    def __le__(self, other: Any) -> bool:
        """Creates the less than or equal to comparison for these objects which includes str, list, and tuple.

        Args:
            other: The object to compare to this object.

        Returns:
            True if this object is less than or equal to to the other objects' version number.

        Raises:
            TypeError: If 'other' is a type that cannot be compared to.
        """
        other = self.cast(other, pass_=True)

        if isinstance(other, Version):
            return self.tuple() <= other.tuple()
        else:
            raise TypeError(f"'<=' not supported between instances of '{str(self)}' and '{str(other)}'")

    @abstractmethod
    def __ge__(self, other: Any) -> bool:
        """Creates the greater than or equal to comparison for these objects which includes str, list, and tuple.

        Args:
            other: The object to compare to this object.

        Returns:
            True if this object is greater than or equal to to the other objects' version number.

        Raises:
            TypeError: If 'other' is a type that cannot be compared to.
        """
        other = self.cast(other, pass_=True)

        if isinstance(other, Version):
            return self.tuple() >= other.tuple()
        else:
            raise TypeError(f"'>=' not supported between instances of '{str(self)}' and '{str(other)}'")

    # Instance Methods
    # Constructors/Destructors
    @abstractmethod
    def construct(self, version: Any = None, ver_name: str | None = None, **kwargs: Any) -> None:
        """Constructs the version object based on inputs

        Args:
            version: An object to derive a version from.
            ver_name: The name of the version type being used.
            **kwargs: More keyword arguments for constructing this object
        """
        self.version_type = self.create_version_type(ver_name)

    # Type Conversion
    @abstractmethod
    def list(self) -> list[Any]:
        """Returns the list representation of the version.

        Returns:
            The list representation of the version.
        """
        pass

    @abstractmethod
    def tuple(self) -> tuple[Any]:
        """Returns the tuple representation of the version.

        Returns:
            The tuple representation of the version.
        """
        pass

    @abstractmethod
    def str(self) -> str:
        """Returns the str representation of the version.

        Returns:
            A str with the version numbers in order.
        """
        return super().__str__()

    # Typing
    def set_version_type(self, name: str) -> None:
        """Creates a new VersionType for this object.

        Args:
            The name of the new VersionType.
        """
        self.version_type = VersionType(name, type(self))
