"""cachinginitmeta.py
A mixin metaclass that implements caching and init functionalities
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
from typing import Any

# Third-Party Packages #

# Local Packages #
from ...metaclasses import InitMeta
from .cachingobjectmeta import CachingObjectMeta


# Definitions #
# Classes #
class CachingInitMeta(InitMeta, CachingObjectMeta):
    """Automatically makes a set of all function that are Timed Caches in the class.

    Args:
        name: The name of this class.
        bases: The parent types of this class.
        namespace: The functions and class attributes of this class.
    """

    # Magic Methods #
    # Construction/Destruction
    def __init__(cls, name: str, bases: tuple[type, ...], namespace: dict[str, Any]) -> None:
        CachingObjectMeta.__init__(cls, name, bases, namespace)
        InitMeta.__init__(cls, name, bases, namespace)
