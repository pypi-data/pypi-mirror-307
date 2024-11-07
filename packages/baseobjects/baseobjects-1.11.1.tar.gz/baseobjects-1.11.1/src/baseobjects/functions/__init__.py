"""__init__.py
functions provides classes for functions and methods.
"""
# Package Header #
from ..header import *

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__


# Imports #
# Local Packages #
from .basedecorator import BaseDecorator
from .singlekwargdispatch import singlekwargdispatch
from .functionregister import FunctionRegister
from .methodregister import MethodRegister
from .callablemultiplexer import CallableMultiplexer, MethodMultiplexer, CallableMultiplexItem, CallableMultiplexObject
from .dynamiccallable import DynamicCallable, DynamicMethod, DynamicFunction
