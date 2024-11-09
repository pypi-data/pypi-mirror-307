"""
Make PyTorch models using generator functions.
"""

__version__ = '0.3.0'

from .layers import *
from .verbose import *
from .utils import *

def __getattr__(name):
    from .factory import make_factory
    return make_factory(name)
