"""warnings.py
Adds additional Warnings.
"""
# Package Header #
from .header import *

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
class TimeoutWarning(Warning):
    """A general warning for timeouts."""

    # Magic Methods #
    # Construction/Destruction
    def __init__(self, name: str = "A function") -> None:
        message = f"{name} timed out"
        super().__init__(message)
