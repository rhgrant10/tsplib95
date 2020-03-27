# -*- coding: utf-8 -*-
import math

from . import models


def load_problem(filepath, special=None):
    """Load a problem at the given filepath.

    :param str filepath: path to a TSPLIB problem file
    :param callable special: special/custom distance function
    :return: problem instance
    :rtype: :class:`~Problem`
    """
    with open(filepath) as f:
        return load_problem_fromstring(f.read(), special=special)


def load_solution(filepath):
    """Load a solution at the given filepath.

    :param str filepath: path to a TSPLIB solution file
    :return: solution instance
    :rtype: :class:`~Solution`
    """
    with open(filepath) as f:
        return load_solution_fromstring(f.read())


def load_problem_fromstring(text, special=None):
    """Load a problem from raw text.

    :param str text: text of a TSPLIB problem
    :param callable special: special/custom distance function
    :return: problem instance
    :rtype: :class:`~Problem`
    """
    return models.StandardProblem.parse(text, special=special)


def load_solution_fromstring(text):
    """Load a solution from raw text.

    :param str text: text of a TSPLIB solution
    :return: solution instance
    :rtype: :class:`~Solution`
    """
    return models.StandardProblem.parse(text)


def parse_degrees(coord):
    """Parse an encoded geocoordinate value into real degrees.

    :param float coord: encoded geocoordinate value
    :return: real degrees
    :rtype: float
    """
    degrees = nint(coord)
    minutes = coord - degrees
    return degrees + minutes * 5 / 3


def nint(x):
    """Round a value to an integer.

    :param float x: original value
    :return: rounded integer
    :rtype: int
    """
    return int(x + 0.5)


def icost(x):
    return int(100 * x + 0.5)


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


def _int_sum(n, memo={}):
    if n not in memo:
        s = n * (n + 1) // 2
        memo[n] = s
    return memo[n]


def integer_sum(n, m=None):
    s = _int_sum(n)
    if m:
        s -= _int_sum(m)
    return s


def pairwise(indexes):
    starts = list(indexes)
    ends = list(indexes)
    ends += [ends.pop(0)]
    return zip(starts, ends)
