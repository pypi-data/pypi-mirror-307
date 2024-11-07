"""dispatchablecomposite.py
A basic composite object which is composed of component objects.
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
from ..objects import DispatchableClass
from .basedispatchingcomposite import BaseDispatchingComposite


# Definitions #
# Classes #
class DispatchableComposite(BaseDispatchingComposite, DispatchableClass):
    """A basic composite object which is composed of component objects.

    Class Attributes:
        default_component_types: The default component classes and their keyword arguments for this object.
        default_components: The default components for this object.

    Attributes:
        components: The components of this object.

    Args:
        component_kwargs: Keyword arguments for creating the components.
        component_types: Component classes and their keyword arguments to instantiate.
        components: Components to add.
        **kwargs: Keyword arguments for inheritance.
    """
