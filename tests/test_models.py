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


@pytest.mark.parametrize('node_coords,normalize,correct', [
    ({2: (0, 0), 4: (0, 0)}, False, [2, 4]),
    ({2: (0, 0), 4: (0, 0)}, True, [0, 1]),
])
def test_get_graph_node_normalization(node_coords, normalize, correct):
    problem = create_problem(node_coords=node_coords)
    graph = problem.get_graph(normalize=normalize)
    assert list(graph.nodes) == correct


@pytest.fixture
def complete_problem():
    return create_problem(
        name='foo',
        comment='bar',
        type='baz',
        dimension=42,
        capacity=11,
        weight_function='EUC2D',
        edge_data_format='EDGE_LIST',
        node_coords={0: (0, 1), 1: (0, 0), 2: (1, 0)},
        edge_data=[(0, 1), (1, 2), (2, 0)],
        display_data={0: (10, 100), 1: (10, 10), 2: (100, 10)},
        depots=[1],
        fixed_edges=[(2, 0)],
        demands={0: 73, 1: 0},
    )


def test_get_graph_metadata(complete_problem):
    G = complete_problem.get_graph()
    assert G.graph == {
        'name': 'foo',
        'comment': 'bar',
        'type': 'baz',
        'dimension': 42,
        'capacity': 11,
    }


@pytest.mark.parametrize('n,metadata', [
    (0, {'coord': (0, 1), 'display': (10, 100), 'demand': 73, 'is_depot': False}),
    (1, {'coord': (0, 0), 'display': (10, 10), 'demand': 0, 'is_depot': True}),
])
def test_get_node_metadata(complete_problem, n, metadata):
    G = complete_problem.get_graph()
    assert G.nodes[n] == metadata


@pytest.mark.parametrize('e,metadata', [
    ((0, 1), {'weight': 1, 'is_fixed': False}),
    ((2, 0), {'weight': 1, 'is_fixed': True}),
])
def test_get_edge_metadata(complete_problem, e, metadata):
    G = complete_problem.get_graph()
    assert G.edges[e] == metadata
