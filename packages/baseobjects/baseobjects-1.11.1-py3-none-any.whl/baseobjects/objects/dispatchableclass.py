"""dispatchableclass.py
An abstract class which dispatches a subclasses or itself.
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
from .registeredclass import RegisteredClass


# Definitions #
# Classes #
class DispatchableClass(RegisteredClass):
    """An abstract class which registers subclasses, allowing subclass dispatching.

    Class Attributes:
        class_register: A register of all subclasses of this class.
        class_register_head: The root class of the registered classes.
        class_registration: Determines if this class/subclass will be added to the register.
        class_register_namespace: The namespace of the subclass.
        class_register_name: The name of which the subclass will be registered as.
    """

    # Class Methods #
    @classmethod
    def get_class_information(cls, *args: Any, **kwargs: Any) -> tuple[str, str, str | None]:
        """Gets a class namespace and name from a given set of arguments.

        Args:
            *args: The arguments to get the namespace and name from.
            **kwargs: The keyword arguments to get the namespace and name from.

        Returns:
            The namespace, name, and optionally the name of the module of the class.
        """
        raise NotImplementedError("This method needs to be implemented to dispatch classes.")

    # Magic Methods #
    # Construction/Destruction
    def __new__(cls, *args: Any, **kwargs: Any) -> RegisteredClass:
        """With given input, will return the correct subclass."""
        if cls is cls.class_register_head and (kwargs or args):
            class_ = cls.get_registered_class(*cls.get_class_information(*args, **kwargs))
            if class_ is not None and class_ is not cls.class_register_head:
                return class_(*args, **kwargs)
        return super().__new__(cls)
