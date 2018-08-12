# -*- coding: utf-8 -*-
import itertools

from . import matrix
from . import distances


def is_explicit(problem):
    return problem['EDGE_WEIGHT_TYPE'] == 'EXPLICIT'


def is_full_matrix(problem):
    return problem.get('EDGE_WEIGHT_FORMAT') == 'FULL_MATRIX'


def is_special(problem):
    return problem['EDGE_WEIGHT_TYPE'] == 'SPECIAL'


def is_complete(problem):
    return 'EDGE_DATA_FORMAT' not in problem


def is_symmetric(problem):
    return not is_full_matrix(problem) and not is_special(problem)


def is_depictable(problem):
    if 'DISPLAY_DATA_SECTION' in problem:
        return True

    if problem.get('DISPLAY_DATA_TYPE') == 'NO_DISPLAY':
        return False

    return 'NODE_COORD_SECTION' in problem


def pairwise(indexes):
    starts = list(indexes)
    ends = list(indexes)
    ends += [ends.pop(0)]
    return zip(starts, ends)


def trace_tours(problem, solution, special=None):
    wfunc = create_weight_function(problem, special=special)

    solutions = []
    for tour in solution['TOUR_SECTION']:
        weight = sum(wfunc(*edge) for edge in pairwise(tour))
        solutions.append(weight)

    return solutions


def create_weight_function(problem, special=None):
    if is_explicit(problem):
        matrix = create_explicit_matrix(problem)
        return lambda i, j: matrix[i, j]
    return create_distance_function(problem, special=special)


def create_distance_function(problem, special=None):
    nodes = problem['NODE_COORD_SECTION']

    if special is None:
        if is_special(problem):
            raise Exception('missing needed special weight function')
        weight_type = problem['EDGE_WEIGHT_TYPE']
        wfunc = distances.TYPES[weight_type]
    else:
        wfunc = special

    def adapter(i, j):
        return wfunc(nodes[i], nodes[j])

    return adapter


def create_explicit_matrix(problem):
    Matrix = matrix.TYPES[problem['EDGE_WEIGHT_FORMAT']]
    weights = problem['EDGE_WEIGHT_SECTION']
    dimension = problem['DIMENSION']
    m = get_min_node_index(problem)
    return Matrix(weights, dimension, min_index=m)


def get_nodes(problem):
    if 'NODE_COORD_SECTION' in problem:
        return list(problem['NODE_COORD_SECTION'])
    elif 'DISPLAY_DATA_SECTION' in problem:
        return list(problem['DISPLAY_DATA_SECTION'])
    elif 'TOUR_SECTION' in problem:
        return list(problem['TOUR_SECTION'])
    else:
        return list(range(problem['DIMENSION']))


def get_edges(problem):
    fmt = problem.get('EDGE_DATA_FORMAT')
    if fmt == 'EDGE_LIST':
        yield from problem['EDGE_DATA_SECTION']
    elif fmt == 'ADJ_LIST':
        for i, adj in problem['EDGE_DATA_SECTION'].items():
            yield from ((i, j) for j in adj)
    else:
        indexes = get_nodes(problem)
        yield from itertools.product(iter(indexes), iter(indexes))


def get_min_node_index(problem):
    return min(get_nodes(problem))


def get_display(problem, i):
    if is_depictable(problem):
        try:
            return problem['DISPLAY_DATA_SECTION'][i]
        except KeyError:
            return problem['NODE_COORD_SECTION'][i]
    else:
        return None
