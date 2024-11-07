"""initmeta.py
InitMeta is an abstract metaclass that implements an init class method which allows some setup after a class is created.
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
from ..bases import BaseMeta


# Definitions #
# Meta Classes #
class InitMeta(BaseMeta):
    """An abstract metaclass that implements an init class method which allows some setup after a class is created.

    Args:
        name: The name of this class.
        bases: The parent types of this class.
        namespace: The functions and class attributes of this class.
    """

    # Magic Methods #
    # Construction/Destruction
    def __init__(cls, name: str, bases: tuple[type, ...], namespace: dict[str, Any]) -> None:
        super().__init__(name, bases, namespace)
        cls._init_class_(name=name, bases=bases, namespace=namespace)

    def _init_class_(
        cls,
        name: str | None = None,
        bases: tuple[type, ...] | None = None,
        namespace: dict[str, Any] | None = None,
    ) -> None:
        pass
