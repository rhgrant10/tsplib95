# -*- coding: utf-8 -*-
from . import parser
from . import models


def load_problem(filepath, special=None):
    data = parser.parse(filepath)
    return models.Problem(special=special, **data)


def load_solution(filepath):
    data = parser.parse(filepath)
    return models.Solution(**data)
