"""automaticproperties.py
An abstract class which creates properties for this class automatically.
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
from collections.abc import Callable, Iterable
from abc import abstractmethod
from builtins import property
from typing import Any

# Third-Party Packages #

# Local Packages #
from ..bases import BaseObject
from ..metaclasses import InitMeta
from ..typing import PropertyCallbacks


# Definitions #
# Classes #
class AutomaticProperties(BaseObject, metaclass=InitMeta):
    """An abstract class which creates properties for this class automatically.

    Class Attributes:
        _properties_map: The functions used to create properties.
        _properies: A container that has the names of the properties and some information to build them.
    """

    # Class Attributes #
    _properties_map_cls: list[Any] = []
    _properties: Any = None

    # Class Methods #
    # Class Construction
    @classmethod
    def _init_class_(
        cls,
        name: str | None = None,
        bases: tuple[type, ...] | None = None,
        namespace: dict[str, Any] | None = None,
    ) -> None:
        """A method that runs after class creation, creating the properties for this class.

        Args:
            name: The name of this class.
            bases: The parent types of this class.
            namespace: The functions and class attributes of this class.
        """
        cls._properties_map: list[Any] = cls._properties_map_cls.copy()

        cls._construct_properties_map()
        cls._construct_properties()

    # Callbacks
    @classmethod
    def _get(cls, obj: Any, name: str) -> Any:
        """A generic get which can be implemented in a subclass.

        Args:
            obj: The target object to get the attribute from.
            name: The name of the attribute to get from the object.

        Returns:
            The item to return.
        """
        return getattr(obj, name)

    @classmethod
    def _set(cls, obj: Any, name: str, value: Any) -> None:
        """A generic set which can be implemented in a subclass.

        Args:
            obj: The target object to set.
            name: The name of the attribute to set.
            value: The item to set within the target object.
        """
        setattr(obj, name, value)

    @classmethod
    def _del(cls, obj: Any, name: str) -> None:
        """A generic delete which can be implemented in a subclass.

        Args:
            obj: The target object to delete an attribute from.
            name: The name of attribute to delete in the object.
        """
        delattr(obj, name)

    # Callback Factories
    @classmethod
    def _default_callback_factory(cls, info: Any) -> PropertyCallbacks:
        """An example factory for creating property modification functions.

        Args:
            info: An object that can be used to create the get, set, and delete functions

        Returns:
            get_: The get function for a property object.
            set_: The wet function for a property object.
            del_: The del function for a property object.
        """
        name = info

        def get_(obj: Any) -> Any:
            """Gets an attribute in the object."""
            return cls._get(obj, name)

        def set_(obj: Any, value) -> None:
            """Sets an attribute in the object."""
            cls._set(obj, name, value)

        def del_(obj: Any) -> None:
            """Deletes an attribute in the object object."""
            cls._del(obj, name)

        return get_, set_, del_

    # Property Constructors
    @classmethod
    def _iterable_to_properties(
        cls, iter_: Iterable[str], callback_factory: Callable[[str], PropertyCallbacks]
    ) -> None:
        """Create properties for this class based on an iterable where the items are the property names.

        Args:
            iter_: The names of the properties which the factories will use to create functions.
            callback_factory: The factory that creates get, set, del, functions for the property.
        """
        for name in iter_:
            if not hasattr(cls, name):
                get_, set_, del_ = callback_factory(name)
                setattr(cls, name, property(get_, set_, del_))

    @classmethod
    def _dictionary_to_properties(
        cls, dict_: dict[str, Any], callback_factory: Callable[[Any], PropertyCallbacks]
    ) -> None:
        """Create properties for this class based on a dictionary where the keys are the property names.

        Args:
            dict_: The names of the properties and some info to help the factory create functions.
            callback_factory: The factory that creates get, set, del, functions for the property.
        """
        for name, info in dict_.items():
            if not hasattr(cls, name):
                get_, set_, del_ = callback_factory(info)
                setattr(cls, name, property(get_, set_, del_))

    # Properties Mapping
    @classmethod
    @abstractmethod
    def _construct_properties_map(cls) -> None:
        """An abstract method that assigns how properties should be constructed."""
        # cls._properties_map.append(["_properties", cls._dictionary_to_properties, cls._default_callback_factory])

    # Properties Constructor
    # Todo: Make map_ better.
    @classmethod
    def _construct_properties(cls, map_: Iterable[Iterable[str, Callable, Callable]] | None = None) -> None:
        """Constructs all properties from a list which maps the properties and their functionality.

        Args:
            map_: A list to map the properties from.

        Raises:
            AttributeError: If an attribute in the map is not in the object.
        """
        if map_ is not None:
            cls._properties_map = map_

        for map_name, constructor, factory in cls._properties_map:
            try:
                properties = getattr(cls, map_name)
                if properties is not None:
                    constructor(properties, factory)
            except AttributeError:
                raise AttributeError("A class attribute is missing")
