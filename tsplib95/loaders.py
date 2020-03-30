# -*- coding: utf-8 -*-
from . import models


def load_problem(filepath, problem_class=None, special=None):
    """Load a problem at the given filepath.

    :param str filepath: path to a TSPLIB problem file
    :param type problem_class: special/custom problem class
    :param callable special: special/custom distance function
    :return: problem instance
    :rtype: :class:`~Problem`
    """
    with open(filepath) as f:
        problem_text = f.read()
    return load_problem_fromstring(problem_text, special=special,
                                   problem_class=problem_class)


def load_problem_fromstring(text, problem_class=None, special=None):
    """Load a problem from raw text.

    :param str text: text of a TSPLIB problem
    :param type problem_class: special/custom problem class
    :param callable special: special/custom distance function
    :return: problem instance
    :rtype: :class:`~Problem`
    """
    Problem = problem_class or models.StandardProblem
    return Problem.parse(text, special=special)
