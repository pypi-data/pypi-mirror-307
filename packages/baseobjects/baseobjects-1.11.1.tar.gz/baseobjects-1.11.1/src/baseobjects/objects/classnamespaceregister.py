"""classnamespaceregister.py

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
from collections.abc import Iterable, Mapping
from copy import deepcopy
from typing import ClassVar, Any

# Third-Party Packages #

# Local Packages #
from ..bases import BaseDict, search_sentinel


# Definitions #
# Classes #
class ClassNamespaceRegister(BaseDict):
    """A register for classes in namespaces.

    Class Attributes:
        default_classes: The default namespaces, classes, and their keyword arguments for this object.

    Args:
        classes: Classes and their namespaces to add, can be an iterable of iterables or a dictionary.
        init: Determines if this object will construct.
        **kwargs: Keyword arguments for inheritance.
    """

    # Attributes #
    default_classes: ClassVar[dict[str, dict[str, tuple[type, dict[str, Any]]]]] = {}

    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        classes: dict[str, dict[str, tuple[type, dict[str, Any]]]] | Iterable | None = None,
        init: bool = True,
        **kwargs: Any
    ) -> None:
        # Parent Attributes #
        super().__init__()

        # New Attributes #
        self.data.update(((n, deepcopy(ns)) for n, ns in self.default_classes.items()))

        # Object Construction #
        if init:
            self.construct(
                classes=classes,
                **kwargs,
            )

    # Instance Methods #
    # Constructors/Destructors
    def construct(
        self,
        classes: dict[str, dict[str, tuple[type, dict[str, Any]]]] | Iterable | None = None,
        **kwargs: Any
    ) -> None:
        """Constructs this object.

        Args:
            classes: Classes to add.
            **kwargs: Keyword arguments for inheritance.
        """
        if isinstance(classes, Mapping):
            self.data.update(((n, deepcopy(ns)) for n, ns in classes.items()))
        elif isinstance(classes, Iterable):
            self.register_classes(classes)

        super().construct(**kwargs)

    # Register
    def register_class(
        self,
        cls: type,
        namespace: str | None = None,
        name: str | None = None,
        class_kwargs: dict[str, Any] | None = None,
    ) -> None:
        """Registers a class with the given namespace and name.

        Args:
            cls: The class to register.
            namespace: The namespace of the subclass.
            name: The name of the subclass.
            class_kwargs: The keyword arguments for creating the class.
        """
        if namespace is None:
            namespace = cls.__dict__.get("_module_", cls.__module__)

        if namespace.split(".")[0] == "src":
            namespace = namespace[4:]

        if name is None:
            name = cls.__name__

        if class_kwargs is None:
            class_kwargs = {}

        namespace_types = self.get(namespace, None)
        if namespace_types is not None:
            namespace_types[name] = cls
        else:
            self.data[namespace] = {name: (cls, class_kwargs)}

    def register_classes(self, classes: Iterable[Iterable]) -> None:
        """Registers multiple classes.

        Args:
            classes: The classes to register as an iterable of the arguments for register_class.
        """
        for cls in classes:
            self.register_class(*cls)

    def update_classes(self, classes: dict[str, dict[str, tuple[type, dict[str, Any]]]]) -> None:
        """Updates the classes.

        Args:
            classes: The namespaces and classes to update.
        """
        self.data.update(((n, deepcopy(ns)) for n, ns in classes.items()))

    def get_class(self, namespace: str, name: str, default: Any = search_sentinel) -> Any:
        """Gets a class from the register.

        Args:
            namespace: The namespace of the subclass.
            name: The name of the class to get.
            default: The default value to return if the class is not found.

        Returns:
            The requested class and its keyword arguments.
        """
        if default is search_sentinel:
            return self.data[namespace][name]
        else:
            return self.data.get(namespace, {}).get(name, default)

    def get_new(
        self,
        namespace: str,
        name: str,
        class_kwargs: dict[str, Any] | None = None,
        default: Any = search_sentinel,
    ) -> Any:
        """Gets a new instance of a class from the register.

        Args:
            namespace: The namespace of the subclass.
            name: The name of the class to get.
            class_kwargs: The keyword arguments for the class.
            default: The default value to return if the class is not found.

        Returns:
            The requested class.
        """
        if default is search_sentinel:
            cls, d_kwargs = self.data[namespace][name]
        elif (item := self.data.get(namespace, {}).get(name, search_sentinel)) is not search_sentinel:
            cls, d_kwargs = item
        else:
            return default

        return cls(**d_kwargs | class_kwargs)
