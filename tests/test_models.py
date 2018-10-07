# -*- coding: utf-8 -*-
from unittest import mock

import pytest

from tsplib95 import models


def create_problem(**kwargs):
    p = models.Problem()
    # set attributes after creation intentionally
    for k, v in kwargs.items():
        setattr(p, k, v)
    return p


@pytest.mark.parametrize('problem,correct', [
    (create_problem(edge_weight_type='EXPLICIT'), True),
    (create_problem(edge_weight_type='FUNCTION'), False),
    (create_problem(edge_weight_type=None), False),
    (create_problem(), False)
])
def test_is_explicit(problem, correct):
    assert problem.is_explicit() is correct


@pytest.mark.parametrize('problem,correct', [
    (create_problem(edge_weight_format='FULL_MATRIX'), True),
    (create_problem(edge_weight_format='UPPER_ROW'), False),
    (create_problem(edge_weight_format=None), False),
    (create_problem(), False)
])
def test_is_full_matrix(problem, correct):
    assert problem.is_full_matrix() is correct


@pytest.mark.parametrize('problem,correct', [
    (create_problem(edge_weight_format='FULL_MATRIX', edge_weight_type='EXPLICIT'), True),
    (create_problem(edge_weight_format='FULL_MATRIX'), True),
    (create_problem(edge_weight_type='EXPLICIT'), True),
    (create_problem(), False)
])
def test_is_weighted(problem, correct):
    assert problem.is_weighted() is correct


@pytest.mark.parametrize('problem,correct', [
    (create_problem(edge_weight_type='SPECIAL'), True),
    (create_problem(edge_weight_type='GEO'), False),
    (create_problem(edge_weight_type=None), False),
    (create_problem(), False)
])
def test_is_special(problem, correct):
    assert problem.is_special() is correct


@pytest.mark.parametrize('problem,correct', [
    (create_problem(edge_data_format='EDGE_LIST'), False),
    (create_problem(edge_data_format='ADJ_LIST'), False),
    (create_problem(edge_data_format=None), True),
    (create_problem(), True)
])
def test_is_complete(problem, correct):
    assert problem.is_complete() is correct


@pytest.mark.parametrize('problem,correct', [
    (create_problem(edge_weight_format='FULL_MATRIX', edge_weight_type='SPECIAL'), False),
    (create_problem(edge_weight_format='UPPER_ROW', edge_weight_type='SPECIAL'), False),
    (create_problem(edge_weight_format='FULL_MATRIX', edge_weight_type='GEO'), False),
    (create_problem(edge_weight_format='UPPER_ROW', edge_weight_type='GEO'), True),
    (create_problem(), True)
])
def test_is_symmetric(problem, correct):
    assert problem.is_symmetric() is correct


@pytest.mark.parametrize('problem,correct', [
    (create_problem(display_data=None, display_data_type=None, node_coords=True), True),
    (create_problem(display_data=None, display_data_type=None, node_coords=None), False),
    (create_problem(display_data=None, display_data_type='NO_DISPLAY', node_coords=True), False),
    (create_problem(display_data=None, display_data_type='NO_DISPLAY', node_coords=None), False),
    (create_problem(display_data=True, display_data_type=None, node_coords=True), True),
    (create_problem(display_data=True, display_data_type=None, node_coords=None), True),
    (create_problem(display_data=True, display_data_type='NO_DISPLAY', node_coords=True), True),
    (create_problem(display_data=True, display_data_type='NO_DISPLAY', node_coords=None), True),
    (create_problem(), False)
])
def test_is_depictable(problem, correct):
    assert problem.is_depictable() is correct


@pytest.mark.parametrize('problem,correct', [
    (create_problem(is_depictable=mock.Mock(return_value=True), display_data=['foo']), 'foo'),
    (create_problem(is_depictable=mock.Mock(return_value=True), node_coords=['bar']), 'bar'),
    (create_problem(is_depictable=mock.Mock(return_value=True), display_data=['foo'], node_coords=['bar']), 'foo'),
    (create_problem(is_depictable=mock.Mock(return_value=False), display_data=['foo'], node_coords=['bar']), None),
    (create_problem(), None),
])
def test_get_display(problem, correct):
    assert problem.get_display(0) is correct
