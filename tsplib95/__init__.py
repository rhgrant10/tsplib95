# -*- coding: utf-8 -*-

"""Top-level package for TSPLIB 95."""

__author__ = """Robert Grant"""
__email__ = 'rhgrant10@gmail.com'
__version__ = '0.6.1'


from . import bisep  # noqa: F401
from . import distances  # noqa: F401
from . import exceptions  # noqa: F401
from . import fields  # noqa: F401
from . import matrix  # noqa: F401
from . import models  # noqa: F401
from . import transformers  # noqa: F401
from . import utils  # noqa: F401

from .models import StandardProblem


parse = StandardProblem.parse
