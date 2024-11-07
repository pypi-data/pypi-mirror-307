"""__init__.py
bases provides several base classes.
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
from .sentinelobject import SentinelObject, search_sentinel
from .baseobject import BaseObject
from .basemeta import BaseMeta
from .basecallable import BaseCallable, BaseMethod, BaseFunction
from .collections import *
