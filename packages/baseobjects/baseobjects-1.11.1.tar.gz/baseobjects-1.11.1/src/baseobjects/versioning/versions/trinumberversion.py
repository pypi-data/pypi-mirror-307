"""trinumberversion.py
TriNumberVersion is a versioning system which is defined by three numbers. This class does not enforce any special
meaning of the three number, but the Major number is more significant than the Minor number which is more
significant than the Patch number. A good example of the tri-number framework can be found at https://semver.org/
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
from collections.abc import Iterable
from typing import Any

# Third-Party Packages #

# Local Packages #
from ...functions import singlekwargdispatch
from ..version import Version


# Definitions #
# Classes #
class TriNumberVersion(Version):
    """A dataclass like class that stores and handles a version number.

    Class Attributes:
        default_version_name: The default name of this version object.

    Attributes:
        major: The major change number of the version.
        minor: The minor change number of the version.
        patch: The patch change number of the version.

    Args:
        version: An object to derive a version from.
        minor: The minor change number of the version.
        patch: The patch change number of the version.
        major: The major change number of the version.
        ver_name : The name of the version type being used.
        init: Determines if this object will construct.
    """

    # Attributes #
    default_version_name: str = "TriNumber"
    major: int = 0
    minor: int = 0
    patch: int = 0

    # Magic Methods
    # Construction/Destruction
    def __init__(
        self,
        version: Iterable[int] | str | int | None = None,
        minor: int | None = None,
        patch: int | None = None,
        major: int | None = None,
        ver_name: str | None = None,
        init: bool = True,
    ) -> None:
        # Parent Attributes #
        super().__init__(init=False)

        # Object Construction #
        if init:
            self.construct(version=version, minor=minor, patch=patch, major=major, ver_name=ver_name)

    # Comparison
    def __eq__(self, other: Any) -> bool:
        """Expands on equals comparison to include comparing the version number.

        Args:
            other: The object to compare to this object.

        Returns:
            True if the other object or version number is equivalent.
        """
        if isinstance(other, TriNumberVersion):
            return self.tuple() == other.tuple()
        elif hasattr(other, "VERSION"):
            return self.tuple() == other.VERSION.tuple()  # Todo: Maybe change the order to be cast friendly
        else:
            try:
                self.tuple() == self.cast(other).tuple()
            except TypeError:
                return super().__eq__(other)

    def __ne__(self, other: Any) -> bool:
        """Expands on not equals comparison to include comparing the version number.

        Args:
            other (:obj:): The object to compare to this object.

        Returns:
            bool: True if the other object or version number is not equivalent.
        """
        if isinstance(other, TriNumberVersion):
            return self.tuple() != other.tuple()
        elif hasattr(other, "VERSION"):
            return self.tuple() != other.VERSION.tuple()
        else:
            try:
                self.tuple() != self.cast(other).tuple()
            except TypeError:
                return super().__ne__(other)

    def __lt__(self, other: Any) -> bool:
        """Creates the less than comparison for these objects which includes str, list, and tuple.

        Args:
            other (:obj:): The object to compare to this object.

        Returns:
            bool: True if this object is less than to the other objects' version number.

        Raises:
            TypeError: If 'other' is a type that cannot be compared to.
        """
        if isinstance(other, TriNumberVersion):
            return self.tuple() < other.tuple()
        elif hasattr(other, "VERSION"):
            return self.tuple() < other.VERSION.tuple()
        else:
            try:
                self.tuple() == self.cast(other).tuple()
            except TypeError:
                raise TypeError(f"'>' not supported between instances of '{str(self)}' and '{str(other)}'")

    def __gt__(self, other: Any) -> bool:
        """Creates the greater than comparison for these objects which includes str, list, and tuple.

        Args:
            other (:obj:): The object to compare to this object.

        Returns:
            bool: True if this object is greater than to the other objects' version number.

        Raises:
            TypeError: If 'other' is a type that cannot be compared to.
        """
        if isinstance(other, TriNumberVersion):
            return self.tuple() > other.tuple()
        elif hasattr(other, "VERSION"):
            return self.tuple() > other.VERSION.tuple()
        else:
            try:
                self.tuple() > self.cast(other).tuple()
            except TypeError:
                raise TypeError(f"'>' not supported between instances of '{str(self)}' and '{str(other)}'")

    def __le__(self, other: Any) -> bool:
        """Creates the less than or equal to comparison for these objects which includes str, list, and tuple.

        Args:
            other (:obj:): The object to compare to this object.

        Returns:
            bool: True if this object is less than or equal to to the other objects' version number.

        Raises:
            TypeError: If 'other' is a type that cannot be compared to.
        """
        if isinstance(other, TriNumberVersion):
            return self.tuple() <= other.tuple()
        elif hasattr(other, "VERSION"):
            return self.tuple() <= other.VERSION.tuple()
        else:
            try:
                self.tuple() <= self.cast(other).tuple()
            except TypeError:
                raise TypeError(f"'<=' not supported between instances of '{str(self)}' and '{str(other)}'")

    def __ge__(self, other: Any) -> bool:
        """Creates the greater than or equal to comparison for these objects which includes str, list, and tuple.

        Args:
            other (:obj:): The object to compare to this object.

        Returns:
            bool: True if this object is greater than or equal to to the other objects' version number.

        Raises:
            TypeError: If 'other' is a type that cannot be compared to.
        """
        if isinstance(other, TriNumberVersion):
            return self.tuple() >= other.tuple()
        elif hasattr(other, "VERSION"):
            return self.tuple() >= other.VERSION.tuple()
        else:
            try:
                self.tuple() >= self.cast(other).tuple()
            except TypeError:
                raise TypeError(f"'>=' not supported between instances of '{str(self)}' and '{str(other)}'")

    # Instance Methods
    # Constructors/Destructors
    def construct(
        self,
        version: Iterable[int] | str | int | None = None,
        minor: int | None = None,
        patch: int | None = None,
        major: int | None = None,
        ver_name: str | None = None,
    ) -> None:
        """Constructs the version object based on inputs.

        Args:
            version: An object to derive a version from.
            minor: The minor change number of the version.
            patch: The patch change number of the version.
            major: The major change number of the version.
            ver_name: The name of the version type being used.
        """
        self.set_version(version=version, minor=minor, patch=patch, major=major)

        super().construct(ver_name)

    @singlekwargdispatch("version")
    def set_version(
        self,
        version: Iterable[int] | str | int | None = None,
        minor: int | None = None,
        patch: int | None = None,
        major: int | None = None,
    ) -> None:
        """Sets the version based on the first input type.

        Args:
            version: An object to derive a version from.
            minor: The minor change number of the version.
            patch: The patch change number of the version.
            major: The major change number of the version.

        Raises:
            TypeError: If the supplied input cannot be used to construct this object.
        """
        raise TypeError(f"{type(self)} cannot set the version with {type(version)}")

    @set_version.register(Iterable)
    def _(self, version: Iterable[int], **kwargs: Any) -> None:
        """Sets the version when given an iterable.

        Args:
            version: The version as an iterable.
            **kwargs: Addition keyword argumnets for setting the version.
        """
        self.major, self.minor, self.patch = version

    @set_version.register
    def _(self, version: str, **kwargs: Any) -> None:
        """Sets the version when given a string.

        Args:
            version: The version as a string.
            **kwargs: Addition keyword argumnets for setting the version.
        """
        ranks = version.split(".")
        for i, r in enumerate(ranks):
            ranks[i] = int(r)
        self.major, self.minor, self.patch = ranks

    @set_version.register
    def _(self, version: int, minor: int | None = None, patch: int | None = None, **kwargs: Any) -> None:
        """Sets the version when given int.

        Args:
            version: The major change number of the version.
            minor: The minor change number of the version.
            patch: The patch change number of the version.
            **kwargs: Addition keyword argumnets for setting the version.
        """
        self.major = version
        if minor is not None:
            self.minor = minor
        if patch is not None:
            self.patch = patch

    @set_version.register
    def _(
        self,
        version: None = None,
        minor: int | None = None,
        patch: int | None = None,
        major: int | None = None,
    ) -> None:
        """Sets the version when given int.

        Args:
            version: The major change number of the version.
            minor: The minor change number of the version.
            patch: The patch change number of the version.
            major: The major change number of the version.
        """
        if major is not None:
            self.major = version
        if minor is not None:
            self.minor = minor
        if patch is not None:
            self.patch = patch

    # Type Conversion
    def list(self) -> list[int, int, int]:
        """Returns the list representation of the version.

        Returns:
            A list with the version numbers in order.
        """
        return [self.major, self.minor, self.patch]

    def tuple(self) -> tuple[int, int, int]:
        """Returns the tuple representation of the version.

        Returns:
            A tuple with the version numbers in order.
        """
        return self.major, self.minor, self.patch

    def str(self) -> str:
        """Returns the str representation of the version.

        Returns:
            A str with the version numbers in order.
        """
        return f"{self.major}.{self.minor}.{self.patch}"
