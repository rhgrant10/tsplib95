# -*- coding: utf-8 -*-

"""Top-level package for TSPLIB 95."""

__author__ = """Robert Grant"""
__email__ = 'rhgrant10@gmail.com'
__version__ = '0.6.1'


from . import bisep  # noqa: F401
from . import distances  # noqa: F401
from . import exceptions  # noqa: F401
from . import fields  # noqa: F401
from . import loaders  # noqa: F401
from . import matrix  # noqa: F401
from . import models  # noqa: F401
from . import transformers  # noqa: F401
from . import utils  # noqa: F401

# text -> problem
parse = models.StandardProblem.parse

# filename -> problem
load = models.StandardProblem.load

# file object -> problem
read = models.StandardProblem.read

# legacy
load_unknown = load_solution = load_problem = loaders.load_problem
load_unknown_fromstring = load_solution_fromstring = load_problem_fromstring = loaders.load_problem_fromstring  # noqa: E501
