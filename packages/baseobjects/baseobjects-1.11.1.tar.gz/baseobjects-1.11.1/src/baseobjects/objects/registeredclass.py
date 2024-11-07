"""registeredclass.py
An abstract class which registers subclasses, allowing subclass dispatching.
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
from importlib import import_module
from typing import ClassVar, Any, Optional
from warnings import warn

# Third-Party Packages #

# Local Packages #
from ..bases import BaseObject


# Definitions #
# Classes #
class RegisteredClass(BaseObject):
    """An abstract class which registers subclasses, allowing subclass dispatching.

    Class Attributes:
        class_register: A register of all subclasses of this class.
        class_register_head: The root class of the registered classes.
        class_registration: Determines if this class/subclass will be added to the register.
        class_register_namespace: The namespace of the subclass.
        class_register_name: The name of which the subclass will be registered as.
    """

    # Class Attributes #
    _module_: ClassVar[str | None] = None

    class_register: ClassVar[dict[str, dict[str, type]] | None] = None
    class_register_head: ClassVar[type["RegisteredClass"] | None] = None
    class_registration: ClassVar[bool] = False
    class_register_namespace: ClassVar[str | None] = None
    class_register_name: ClassVar[str | None] = None

    # Class Methods #
    # Construction/Destruction
    def __init_subclass__(cls, namespace: str | None = None, name: str | None = None, **kwargs: Any) -> None:
        """The init when creating a subclass.

        Args:
            **kwargs: The keyword arguments for creating a subclass.
        """
        super().__init_subclass__(**kwargs)

        # Add subclass to the register.
        if cls.class_registration:
            if cls.class_register is None:
                raise NotImplementedError("The root registered class must create a register.")

            if not cls.class_register:
                cls.class_register_head = cls

            cls.register_class(namespace=namespace or cls.class_register_namespace, name=name)

    # Register
    @classmethod
    def register_class(cls, namespace: str | None = None, name: str | None = None) -> None:
        """Registers this class with the given namespace and name.

        Args:
            namespace: The namespace of the subclass.
            name: The name of the subclass.
        """
        if "class_register_namespace" not in cls.__dict__ or namespace is not None:
            if namespace is None:
                namespace = cls.__dict__.get("_module_", cls.__module__)
            cls.class_register_namespace = namespace[4:] if namespace.split(".")[0] == "src" else namespace

        if "class_register_name" not in cls.__dict__ or name is not None:
            cls.class_register_name = cls.__name__ if name is None else name

        namespace_types = cls.class_register.get(cls.class_register_namespace, None)
        if namespace_types is not None:
            namespace_types[cls.class_register_name] = cls
        else:
            cls.class_register[cls.class_register_namespace] = {cls.class_register_name: cls}

    @classmethod
    def get_registered_class(cls, namespace: str, name: str, module: str | None = None) -> Optional["RegisteredClass"]:
        """Gets a subclass from the register.

        Args:
            namespace: The namespace of the subclass.
            name: The name of the subclass to get.
            module: The module to import if the subclass is not found.

        Returns:
            The requested subclass.
        """
        if (namespace_types := cls.class_register.get(namespace, None)) is None and module is not None:
            try:
                import_module(module)
            except Exception as e:
                warn(f"Failed to import module '{module}' with error: {e}, skipping.")
            else:
                namespace_types = cls.class_register.get(namespace, None)

        if namespace_types is None:
            return None
        elif (class_ := namespace_types.get(name, None)) is None and module is not None:
            try:
                import_module(module)
            except Exception as e:
                warn(f"Failed to import module '{module}' with error: {e}, skipping.")
            else:
                class_ = namespace_types.get(name, None)

        return class_
