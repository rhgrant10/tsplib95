# -*- coding: utf-8 -*-
import pytest

from tsplib95 import distances


PROBLEMS = {
    ((3, 4), (3, 4)): {
        'euclidean': 0,
        'manhattan': 0,
        'maximum': 0,
    },
    ((0, 0), (3, 4)): {
        'euclidean': 5,
        'manhattan': 7,
        'maximum': 4,
    },
    ((-3, -4), (3, 4)): {
        'euclidean': 10,
        'manhattan': 14,
        'maximum': 8,
    },
    ((0, 0), (3, 0)): {
        'euclidean': 3,
        'manhattan': 3,
        'maximum': 3,
    },
    ((0, 0), (0, 4)): {
        'euclidean': 4,
        'manhattan': 4,
        'maximum': 4,
    },
}


def get_problems(name):
    return [(s, e, d[name]) for (s, e), d in PROBLEMS.items()]


@pytest.mark.parametrize('start,end,distance', get_problems('euclidean'))
def test_euclidean(start, end, distance):
    assert distances.euclidean(start, end) == distance


@pytest.mark.parametrize('start,end,distance', get_problems('manhattan'))
def test_manhattan(start, end, distance):
    assert distances.manhattan(start, end) == distance


@pytest.mark.parametrize('start,end,distance', get_problems('maximum'))
def test_maximum(start, end, distance):
    assert distances.maximum(start, end) == distance
