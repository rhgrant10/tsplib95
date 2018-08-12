# -*- coding: utf-8 -*-
import math

from . import parser
from . import models


def load_problem(filepath, special=None):
    data = parser.parse(filepath)
    return models.Problem(special=special, **data)


def load_solution(filepath):
    data = parser.parse(filepath)
    return models.Solution(**data)


def parse_degrees(coord):
    degrees = nint(coord)
    minutes = coord - degrees
    return degrees + minutes * 5 / 3


def nint(x):
    return int(x + 0.5)


def deltas(start, end):
    return (e - s for e, s in zip(end, start))


class RadianGeo:
    def __init__(self, coord):
        x, y = coord
        self.lat = self.__class__.parse_component(x)
        self.lng = self.__class__.parse_component(y)

    @staticmethod
    def parse_component(component):
        return math.radians(parse_degrees(component))
