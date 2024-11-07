"""sentinelobject.py
An object which acts as a sentinel object.
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

# Third-Party Packages #

# Local Packages #


# Definitions #
# Classes #
class SentinelObject:
    """An object which acts as a sentinel object.

    Attributes:
        id_number: The id of this sentinel.

    Args:
        id_: The id of this sentinel.
        encoding: The string encoding to use when given a string ID.
        errors: The string encoding errors to use when given a string ID.
    """

    # Attributes #
    id_number: int

    # Magic Methods #
    # Construction/Destruction
    def __init__(self, id_: str | bytes | int, encoding: str = "utf-8", errors: str = "strict") -> None:
        if isinstance(id_, str):
            self.id_number = int.from_bytes(id_.encode(encoding, errors))
        elif isinstance(id_, bytes):
            self.id_number = int.from_bytes(id_)
        elif isinstance(id_, int):
            self.id_number = id_

    # Representation
    def __hash__(self) -> int:
        """Overrides hash to make the object hashable.

        Returns:
            The system ID of the object.
        """
        return id(self)

    # Comparison
    def __eq__(self, other: "SentinelObject") -> bool:
        """Expands on equals comparison to include comparing the ID number.

        Args:
            other: The object to compare to this object.

        Returns:
            True if the other sentinel is equivalent.
        """
        return isinstance(other, SentinelObject) and self.id_number == other.id_number


# Names #
search_sentinel = SentinelObject("search_sentinel")
