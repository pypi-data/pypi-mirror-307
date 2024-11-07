"""basedispatchingcomposite.py
A composite object which includes methods for dispatching component objects during instantiation.
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

# Local Packages
from ..objects import ClassNamespaceRegister
from .basecomposite import BaseComposite


# Definitions #
# Classes #
class BaseDispatchingComposite(BaseComposite):
    """A composite object which includes methods for dispatching component objects during instantiation.

    Class Attributes:
        default_component_types: The default component classes and their keyword arguments for this object.

    Attributes:
        component_types_register: A register of component classes and their keyword arguments.
        components: The components of this object.

    Args:
        component_kwargs: Keyword arguments for creating the components.
        component_types: Component classes and their keyword arguments to instantiate.
        components: Components to add.
        **kwargs: Keyword arguments for inheritance.
    """

    # Attributes #
    component_types_register: ClassNamespaceRegister

    # Methods #
    def dispatch_component_types(self, *args: Any, **kwargs: Any) -> dict[str, tuple[type, dict[str, Any]]]:
        """An abstract method that dispatches component types using the given arguments.

        Args:
            *args: The arguments to use in dispatching.
            **kwargs: The keyword arguments to use in dispatching.

        Returns:
            A dictionary of the names of the components, their types, and their keyword arguments.
        """
        raise NotImplementedError("This method needs to be set to dispatch component types.")
