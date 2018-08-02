# -*- coding: utf-8 -*-

"""Top-level package for TSPLIB 95."""

__author__ = """Robert Grant"""
__email__ = 'rhgrant10@gmail.com'
__version__ = '0.1.0'


from .parser import parse  # noqa: F401
from .utils import trace_tours  # noqa: F401
from .networkx import convert as to_networkx  # noqa: F401
