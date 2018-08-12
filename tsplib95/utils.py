# -*- coding: utf-8 -*-
from . import parser
from . import models


def load_problem(filepath):
    data = parser.parse(filepath)
    return models.Problem(**data)


def load_solution(filepath):
    data = parser.parse(filepath)
    return models.Solution(**data)
