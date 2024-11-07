"""staticwrapper.py
StaticWrapper calls wrapped attributes/functions by creating property descriptor objects for each of the wrapped objects'
attributes/functions. There some limitations to how StaticWapper can be used. First, for any given subclass of
StaticWrapper all object instances must contain the same wrapped object types because descriptor are handled at the
class scope. Second, creating property descriptors does not happen automatically, creation must be invoked though the
_wrap method. This means a subclass must call _wrap to initialize at some point. Also, if the wrapped objects create new
attributes/functions afterwards, then _wrap or _rewrap must be called to add the new attributes/functions. Overall, this
means subclasses should be designed to wrap the same objects and be used to wrap objects that do not create new
attributes/functions after initialization. These limitation are strict, but it leads to great performance preservation
when compared to normal object attribute/method access.
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
from builtins import property
from types import MethodDescriptorType
from typing import Any

# Third-Party Packages #

# Local Packages #
from ..bases import BaseObject
from ..metaclasses import InitMeta
from ..typing import AnyCallable, PropertyCallbacks


# Definitions #
# Functions #
def _get_temp_attributes(obj: "StaticWrapper", name: str) -> None:
    """Creates temporary attributes from a wrapped object.

    Args:
        obj: The wrapping object with the object to get the temporary attributes from.
        name: The attribute name of the wrapped object.
    """
    sub = getattr(obj, name)
    wrapped = obj._wrapped_attributes[name]
    for attribute in wrapped:
        try:
            setattr(obj, "__" + attribute + "_", getattr(sub, attribute))
        except AttributeError:
            continue


def _set_temp_attributes(obj: "StaticWrapper", new: Any, name: str) -> None:
    """Sets a wrapped object's attributes from temporary attributes.

    Args:
        obj: The wrapping object to get the temporary attributes from.
        new: The new object to set the attributes of.
        name: The attribute name of the wrapped object.
    """
    wrapped = obj._wrapped_attributes[name]
    for attribute in wrapped:
        try:
            if hasattr(new, attribute):
                setattr(new, attribute, getattr(obj, "__" + attribute + "_"))
                delattr(obj, "__" + attribute + "_")
        finally:
            continue


# Classes #
class StaticWrapper(BaseObject, metaclass=InitMeta):
    """An object that can call the attributes/functions of embedded objects, acting as if it is inheriting from them.

    Attribute/method resolution of this object will first look with the object itself then it look within the wrapped
    objects' attributes/functions. The resolution order of the wrapped objects is based on _wrap_attributes, first element
    to last.

    This object does not truly use method resolution, but instead creates property descriptors that call the
    attributes/functions of the wrapped objects. To create the property descriptors the _wrap method must be called after
    the objects to wrap are store in this object. Keep in mind, all objects of this class must have the same type of
    wrapped objects, because descriptors are on the class scope. Additionally, this object cannot detect when wrapped
    objects create new or delete attributes/functions. Therefore, subclasses or the user must decide when to call _wrap to
    ensure all the attributes/functions are present. This object is best used to wrap frozen objects or ones that do not
    create or delete attributes/functions after initialization.

    If the objects to wrap can be defined during class instantiation then this class can setup the wrapping by listing
    the types or objects in _wrapped_types. The setup will occur immediately after class instantiation.

    Class Attributes:
        __original_dir_set: The dir of the original wrapper class.
        _get_previous_wrapped: Determines if temporary attributes should be made from the previous wrapped object
        _set_next_wrapped: Determines if temporary attributes should be passed to the next wrapped object.
        _wrapped_types: A list of either types or objects to setup wrapping for.
        _wrap_attributes: Attribute names that will contain the objects to wrap where the resolution order is descending
            inheritance.
        _exclude_attributes: The names of the attributes to exclude from wrapping.
        _wrapped_attributes: The names of the attributes to wrap.
    """

    __original_dir_set: set[str] | None = None
    _get_previous_wrapped: bool = False
    _set_next_wrapped: bool = True
    _wrapped_types: list[Any] = []
    _wrap_attributes: list[str] = []
    _exclude_attributes: set[str] = {"__slotnames__"}
    _wrapped_attributes: dict[str, set[str]] = {}

    # Class Methods #
    # Class Construction
    @classmethod
    def _init_class_(
        cls,
        name: str | None = None,
        bases: tuple[Any, ...] | None = None,
        namespace: dict[str, Any] | None = None,
    ) -> None:
        """A method that runs after class creation, creating the original dir as a set and sets up wrapping."""
        cls.__original_dir_set = set(dir(cls))
        cls._class_wrapping_setup()

    # Callbacks for Accessing a Wrapped Object
    @classmethod
    def _get_wrapped(cls, obj: Any, name: str) -> Any:
        """Gets a wrapped object from the target object's attribute.

        Args:
            obj: The target object to get the wrapped object from.
            name: The attribute name to get the wrapped object from.

        Returns:
            The wrapped object.
        """
        return getattr(obj, name)

    @classmethod
    def _set_wrapped(cls, obj: Any, name: str, value: Any) -> None:
        """Sets the target object's attribute to be a wrapped object.

        Args:
            obj: The target object to set.
            name: The attribute name to set the wrapped object to.
            value: The wrapped object.
        """
        setattr(obj, name, value)

    @classmethod
    def _del_wrapped(cls, obj: Any, name: str) -> None:
        """Deletes the target object's attribute which stores a wrapped object.

        Args:
            obj: The target object to delete.
            name: The attribute name to delete the wrapped object to.
        """
        delattr(obj, name)

    # Callbacks for Accessing a Wrapped Object's Attributes
    @classmethod
    def _get_attribute(cls, obj: Any, wrap_name: str, attr_name: str) -> Any:
        """Gets an attribute from a wrapped object.

        Args:
            obj: The target object to get the wrapped object from.
            wrap_name: The attribute name of the wrapped object.
            attr_name: The attribute name of the attribute to get from the wrapped object.

        Returns:
            The wrapped object.
        """
        return getattr(getattr(obj, wrap_name), attr_name)

    @classmethod
    def _set_attribute(cls, obj: Any, wrap_name: str, attr_name: str, value: Any) -> None:
        """Sets an attribute in a wrapped object.

        Args:
            obj: The target object to set.
            wrap_name: The attribute name of the wrapped object.
            attr_name: The attribute name of the attribute to set from the wrapped object.
            value: The object to set the wrapped objects attribute to.
        """
        setattr(getattr(obj, wrap_name), attr_name, value)

    @classmethod
    def _del_attribute(cls, obj: Any, wrap_name: str, attr_name: str) -> None:
        """Deletes an attribute in a wrapped object.

        Args:
            obj: The target object to set.
            wrap_name: The attribute name of the wrapped object.
            attr_name: The attribute name of the attribute to delete from the wrapped object.

        Raises:
            AttributeError: If the attribute cannot be deleted or does not exist.
        """
        try:
            delattr(getattr(obj, wrap_name), attr_name)
        except AttributeError as error:
            if not hasattr(obj, wrap_name):
                raise error

    @classmethod
    def _evaluate_method(cls, obj: Any, wrap_name: str, method_name: str, args: Any, kwargs: dict[str, Any]) -> Any:
        """Evaluates a method from a wrapped object.

        Args:
            obj: The target object to get the wrapped object from.
            wrap_name: The attribute name of the wrapped object.
            method_name: The method name of the method to get from the wrapped object.
            args: The args of the method to evaluate.
            kwargs: The keyword arguments of the method to evaluate.

        Returns:
            The return of the wrapped object's method.
        """
        return getattr(getattr(obj, wrap_name), method_name)(*args, **kwargs)

    # Callback Factories
    @classmethod
    def _create_wrapping_functions(cls, wrap_name: str) -> PropertyCallbacks:
        """A factory for creating property modification functions for the wrapped objects.

        Args:
            wrap_name: The attribute name of the wrapped object.

        Returns:
            get_: The get function for a property object.
            set_: The wet function for a property object.
            del_: The del function for a property object.
        """
        store_name = "_" + wrap_name  # The true name of the attribute where the wrapped object is stored.

        def get_(obj: Any) -> Any:
            """Gets the wrapped object."""
            return cls._get_wrapped(obj, store_name)

        def set_(obj: Any, value: Any) -> None:
            """Sets the wrapped object, copying the old object's attributes."""
            # Get old attributes
            try:
                if obj._get_previous_wrapped:
                    _get_temp_attributes(obj, wrap_name)
            except AttributeError:
                pass

            # Set new attributes
            try:
                if obj._set_next_wrapped:
                    _set_temp_attributes(obj, value, wrap_name)
            except AttributeError:
                pass

            cls._set_wrapped(obj, store_name, value)

        def del_(obj: Any) -> None:
            """Deletes the wrapped object, storing its attributes for the next object."""
            # Get old attributes
            try:
                if obj._get_previous_wrapped:
                    _get_temp_attributes(obj, wrap_name)
            except AttributeError:
                pass

            cls._del_wrapped(obj, store_name)

        return get_, set_, del_

    @classmethod
    def _create_attribute_functions(cls, wrap_name: str, attr_name: str) -> PropertyCallbacks:
        """A factory for creating property modification functions for accessing a wrapped objects' attributes.

        Args:
            wrap_name (str): The attribute name of the wrapped object.
            attr_name (str): The attribute name of the attribute to modify from the wrapped object.

        Returns:
            get_: The get function for a property object.
            set_: The wet function for a property object.
            del_: The del function for a property object.
        """
        store_name = "_" + wrap_name  # The true name of the attribute where the wrapped object is stored.

        def get_(obj):
            """Gets the wrapped object's attribute and check the temporary attribute if not."""
            try:
                return cls._get_attribute(obj, store_name, attr_name)
            except AttributeError as error:
                try:
                    return getattr(obj, "__" + attr_name + "_")
                except AttributeError:
                    raise error

        def set_(obj, value):
            """Sets the wrapped object's attribute or saves it to a temporary attribute if wrapped object."""
            try:
                cls._set_attribute(obj, store_name, attr_name, value)
            except AttributeError as error:
                if not hasattr(obj, store_name) or getattr(obj, store_name) is None:
                    setattr(obj, "__" + attr_name + "_", value)
                else:
                    raise error

        def del_(obj):
            """Deletes the wrapped object's attribute."""
            cls._del_attribute(obj, store_name, attr_name)

        return get_, set_, del_

    @classmethod
    def _create_method_function(cls, wrap_name: str, attr_name: str) -> AnyCallable:
        """A factory for creating method functions for accessing a wrapped objects' methods.

        Args:
            wrap_name: The attribute name of the wrapped object.
            attr_name: The attribute name of the attribute to modify from the wrapped object.

        Returns:
            The function for a method.
        """
        store_name = "_" + wrap_name  # The true name of the attribute where the wrapped object is stored.

        def func_(obj, *args, **kwargs):
            """Evaluates the wrapped object's method."""
            return cls._evaluate_method(obj, store_name, attr_name, args, kwargs)

        return func_

    # Wrapping
    @classmethod
    def _class_wrapping_setup(cls) -> None:
        """Sets up the class by wrapping what is in _wrapped_types."""
        if cls._wrapped_types:
            try:
                cls._class_wrap(cls._wrapped_types)
            except IndexError:
                raise IndexError("_wrapped_types must be the same length as _wrap_attributes")

    @classmethod
    def _class_wrap(cls, objects: list[Any]) -> None:
        """Adds attributes from embedded objects as properties.

        Args:
           objects: A list of objects or types this object will wrap. Must be in the same order as _wrap_attributes.
        """
        if len(objects) != len(cls._wrap_attributes):
            raise IndexError("objects must be the same length as _wrap_attributes")

        remove = cls.__original_dir_set.union(cls._exclude_attributes)
        for name, obj in zip(cls._wrap_attributes, objects):
            if obj is not None:
                # Set wrapped property
                get_, set_, del_ = cls._create_wrapping_functions(name)
                setattr(cls, name, property(get_, set_, del_))

                # Set attributes properties
                obj_set = set(dir(obj))
                cls._wrapped_attributes[name] = add_dir = obj_set - remove
                remove = obj_set | remove
                for attribute in add_dir:
                    if isinstance(getattr(obj, attribute), MethodDescriptorType):
                        item = cls._create_method_function(name, attribute)
                    else:
                        item = property(*cls._create_attribute_functions(name, attribute))
                    setattr(cls, attribute, item)

    @classmethod
    def _unwrap(cls) -> None:
        """Removes all attributes added from other objects."""
        for name in set(dir(cls)) - cls.__original_dir_set:
            if isinstance(getattr(cls, name, None), property):
                delattr(cls, name)

    @classmethod
    def _class_rewrap(cls, objects: list[Any]) -> None:
        """Removes all the attributes added from other objects then adds attributes from embedded the objects.

        Args:
            objects: A list of objects or types this object will wrap. Must be in the same order as _wrap_attributes.
        """
        cls._unwrap()
        cls._class_wrap(objects)

    # Instance Methods #
    # Wrapping
    def _wrap(self) -> None:
        """Adds attributes from embedded objects as properties."""
        remove = self.__original_dir_set | self._exclude_attributes
        for name in self._wrap_attributes:
            # Get object to wrap
            try:
                obj = getattr(self, name)
                delattr(self, name)  # Delete attribute to be replaced by property
            except AttributeError:
                continue

            if obj is not None:
                # Set wrapped property
                get_, set_, del_ = self._create_wrapping_functions(name)
                setattr(type(self), name, property(get_, set_, del_))
                setattr(self, "_" + name, obj)

                # Set attributes properties
                obj_set = set(dir(obj))
                self._wrapped_attributes[name] = add_dir = obj_set - remove
                remove = obj_set | remove
                for attribute in add_dir:
                    # Reassign attribute storage location
                    if hasattr(self, attribute):
                        setattr(self, "__" + attribute + "_", getattr(self, attribute))
                        try:
                            delattr(self, attribute)
                        except AttributeError:
                            delattr(self, "__" + attribute + "_")
                    # Create property
                    get_, set_, del_ = self._create_attribute_functions(name, attribute)
                    setattr(type(self), attribute, property(get_, set_, del_))

    def _rewrap(self) -> None:
        """Removes all the attributes added from other objects then adds attributes from embedded the objects."""
        self._unwrap()
        self._wrap()

    def _get_temp_attributes(self, name: str) -> None:
        """Creates temporary attributes from a wrapped object.

        Args:
            name: The attribute name of the wrapped object.
        """
        sub = getattr(self, name)
        wrapped = self._wrapped_attributes[name]
        for attribute in wrapped:
            try:
                setattr(self, "__" + attribute + "_", getattr(sub, attribute))
            except AttributeError:
                pass

    def _set_temp_attributes(self, new: str, name: str) -> None:
        """Sets a wrapped object's attributes from temporary attributes.

        Args:
            new: The new object to set the attributes of.
            name: The attribute name of the wrapped object.
        """
        wrapped = self._wrapped_attributes[name]
        for attribute in wrapped:
            if hasattr(new, attribute):
                try:
                    setattr(new, attribute, getattr(self, "__" + attribute + "_"))
                    delattr(self, "__" + attribute + "_")
                except AttributeError:
                    pass
