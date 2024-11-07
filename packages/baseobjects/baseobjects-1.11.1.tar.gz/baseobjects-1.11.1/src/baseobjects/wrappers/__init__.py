"""__init__.py
Abstract classes for objects that can wrap any objects and make their attributes/functions accessible from the wrapper.

StaticWrapper and DynamicWrapper are solutions for two different case. StaticWrapper should be used when
if the application is within the limitations StaticWrapper. DynamicWrapper would be used if the application involves
wrapping various indeterminate object types and/or if the objects change available attributes/functions frequently.

Here are some tested relative performance metrics to highlight those differences: let normal attribute access be 1, when
StaticWrapper accesses a wrapped attribute it takes about 1.7 while DynamicWrapper takes about 4.4. StaticWrapper's
performance loss is debatable depending on the application, but DynamicWrapper takes about x4 longer a normal attribute
access which is not great for most applications.

Todo: add magic method support for StaticWrapper and DynamicWrapper (requires thorough method resolution handling)
"""
# Package Header #
from ..header import *

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__


# Imports
# Local Packages #
from .staticwrapper import StaticWrapper
from .dynamicwrapper import DynamicWrapper
