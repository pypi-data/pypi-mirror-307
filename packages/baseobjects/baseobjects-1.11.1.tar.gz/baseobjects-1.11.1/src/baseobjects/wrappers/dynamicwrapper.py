"""dynamicwrapper.py
DynamicWrapper calls wrapped attribute functions by changing the __getattribute__ method to check the wrapped classes
after checking itself. This makes DynamicWrapper very flexible with its wrapped objects. DynamicWrapper does not have
any usage limitation, but it is significantly slower than normal object attribute/method access, because it handles
every get, set, and delete. Performance would be better if DynamicWrapper was written in C.
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
class DynamicWrapper(BaseObject):
    """An object that can call the attributes/functions of embedded objects, acting as if it is inheriting from them.

    When an object of this class has an attribute/method call it will call a listed object's attribute/method. This is
    similar to what an @property decorator can do but without having to write a decorator for each attribute. Attribute/
    method calling is done dynamically where the objects in the list can change during runtime so the available
    attributes/functions will change based on the objects in the list. Since the available attributes/functions cannot be
    evaluated until runtime, an IDE's auto-complete cannot display all the callable options.

    _attribute_as_parents is the list of attributes of this object that contains the objects that will be used for the
    dynamic calling. This class and subclasses can still have its own defined attributes and functions that are called.
    Which attribute/method is used for the call is handled in the same manner as inheritance where it will check if the
    attribute/method is present in this object, if not it will check in the next object in the list. Therefore, it is
    important to ensure the order of _attribute_as_parents is the order of descending inheritance.

    Class Attributes:
        _wrap_attributes: The list of attribute names that will contain the objects to dynamically wrap where the order
            is descending inheritance.
    """

    _wrap_attributes: list[str] = []

    # Magic Methods #
    # Attribute Access
    def __getattr__(self, name: str) -> Any:
        """Gets the attribute of another object if that attribute is not present in this object.

        Args:
            name: The name of the attribute to get.

        Returns:
            obj: Whatever the attribute contains.

        Raises:
            AttributeError: If the requested attribute cannot be returned.
        """
        # Iterate through all object parents to find the attribute
        for attribute in self._wrap_attributes:
            try:
                return getattr(object.__getattribute__(self, attribute), name)
            except AttributeError:
                pass

        raise AttributeError

    def __setattr__(self, name: str, value: Any) -> None:
        """Sets the attribute of another object if that attribute name is not present in this object.

        Args:
            name: The name of the attribute to set.
            value: Whatever the attribute will contain.
        """
        # Check if item is in self and if not check in object parents
        if name not in self._wrap_attributes and name not in dir(self):
            # Iterate through all indirect parents to find attribute
            for attribute in self._wrap_attributes:
                if attribute in dir(self):
                    parent_object = getattr(self, attribute)
                    if name in dir(parent_object):
                        return setattr(parent_object, name, value)

        # If the item is an attribute in self or not in any indirect parent set as attribute
        object.__setattr__(self, name, value)

    def __delattr__(self, name: str) -> None:
        """Deletes the attribute of another object if that attribute name is not present in this object.

        Args:
            name: The name of the attribute to delete.
        """
        # Check if item is in self and if not check in object parents
        if name not in self._wrap_attributes and name not in dir(self):
            # Iterate through all indirect parents to find attribute
            for attribute in self._wrap_attributes:
                if attribute in dir(self):
                    parent_object = getattr(self, attribute)
                    if name in dir(parent_object):
                        return delattr(parent_object, name)

        # If the item is an attribute in self or not in any indirect parent set as attribute
        object.__delattr__(self, name)

    # Instance Methods #
    # Attribute Access
    def _setattr(self, name: str, value: Any):
        """An override method that will set an attribute of this object without checking its presence in other objects.

        This is useful for setting new attributes after class the definition.

        Args:
            name: The name of the attribute to set.
            value: Whatever the attribute will contain.
        """
        super().__setattr__(name, value)
