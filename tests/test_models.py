# -*- coding: utf-8 -*-
from unittest import mock

import pytest

from tsplib95 import models


def SPECIAL(i, j):
    return 1


def create_problem(**kwargs):
    return models.StandardProblem(**kwargs)


@pytest.fixture
def create_special_problem():
    def create(**kwargs):
        kwargs.setdefault('dimension', 3)
        return models.StandardProblem(**kwargs)
    return create


@pytest.mark.parametrize('typ,fmt,correct', [
    ('EXPLICIT', 'FULL_MATRIX', True),
    ('EXPLICIT', 'UPPER_ROW', True),
    ('EUC_2D', 'FUNCTION', False),
    (None, None, False),
])
def test_is_explicit(create_special_problem, typ, fmt, correct):
    problem = create_special_problem(edge_weight_format=fmt, edge_weight_type=typ)
    assert problem.is_explicit() is correct


@pytest.mark.parametrize('typ,fmt,correct', [
    ('EXPLICIT', 'FULL_MATRIX', True),
    ('EXPLICIT', 'UPPER_ROW', False),
    (None, None, False),
])
def test_is_full_matrix(create_special_problem, typ, fmt, correct):
    problem = create_special_problem(edge_weight_format=fmt, edge_weight_type=typ)
    assert problem.is_full_matrix() is correct


@pytest.mark.parametrize('typ,fmt,special,correct', [
    ('EXPLICIT', 'FULL_MATRIX', None, True),
    ('EXPLICIT', 'LOWER_COL', None, True),
    ('SPECIAL', 'FUNCTION', SPECIAL, True),
    (None, None, None, False),
])
def test_is_weighted(create_special_problem, typ, fmt, special, correct):
    problem = create_special_problem(edge_weight_format=fmt,
                                     edge_weight_type=typ,
                                     special=special)
    assert problem.is_weighted() is correct


@pytest.mark.parametrize('typ,fmt,special,correct', [
    ('SPECIAL', 'FUNCTION', SPECIAL, True),
    ('GEO', 'FUNCTION', None, False),
    (None, None, None, False),
])
def test_is_special(create_special_problem, typ, fmt, special, correct):
    problem = create_special_problem(edge_weight_format=fmt,
                                     edge_weight_type=typ,
                                     special=special)
    assert problem.is_special() is correct


@pytest.mark.parametrize('fmt,correct', [
    ('EDGE_LIST', False),
    ('ADJ_LIST', False),
    (None, True),
])
def test_is_complete(create_special_problem, fmt, correct):
    problem = create_special_problem(edge_data_format=fmt)
    assert problem.is_complete() is correct


@pytest.mark.parametrize('typ,fmt,special,correct', [
    ('EXPLICIT', 'FULL_MATRIX', None, False),
    ('EXPLICIT', 'UPPER_ROW', None, True),
    ('SPECIAL', 'FUNCTION', SPECIAL, False),
    ('GEO', 'FUNCTION', None, True),
    (None, None, None, True),
])
def test_is_symmetric(create_special_problem, typ, fmt, special, correct):
    problem = create_special_problem(edge_weight_format=fmt,
                                     edge_weight_type=typ,
                                     special=special)
    assert problem.is_symmetric() is correct


@pytest.mark.parametrize('dat,typ,nc,correct', [
    (None, None, True, True),
    (None, None, None, False),
    (None, 'NO_DISPLAY', True, False),
    (None, 'NO_DISPLAY', None, False),
    (True, None, True, True),
    (True, None, None, True),
    (True, 'NO_DISPLAY', True, True),
    (True, 'NO_DISPLAY', None, True),
    (None, None, None, False)
])
def test_is_depictable(create_special_problem, dat, typ, nc, correct):
    problem = create_special_problem(display_data=dat,
                                     display_data_type=typ,
                                     node_coords=nc)
    assert problem.is_depictable() is correct


@pytest.mark.parametrize('idp,kw,correct', [
    (True, {'display_data': ['foo']}, 'foo'),
    (True, {'node_coords': ['bar']}, 'bar'),
    (True, {'display_data': ['foo'], 'node_coords': ['bar']}, 'foo'),
    (False, {'display_data': ['foo'], 'node_coords': ['bar']}, None),
    (None, {}, None),
])
def test_get_display(create_special_problem, idp, kw, correct):
    kwargs = {'is_depictable': mock.Mock(return_value=idp), **kw}
    problem = create_special_problem(**kwargs)
    assert problem.get_display(0) is correct


@pytest.mark.parametrize('node_coords,normalize,correct', [
    ({2: (0, 0), 4: (0, 0)}, False, [2, 4]),
    ({2: (0, 0), 4: (0, 0)}, True, [0, 1]),
])
def test_get_graph_node_normalization(create_special_problem, node_coords, normalize, correct):
    problem = create_special_problem(node_coords=node_coords)
    graph = problem.get_graph(normalize=normalize)
    assert list(graph.nodes) == correct


@pytest.fixture
def complete_problem(create_special_problem):
    return create_special_problem(
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
    (0, {'coord': (0, 1), 'display': (10, 100), 'demand': 73, 'is_depot': False}),  # noqa: E501
    (1, {'coord': (0, 0), 'display': (10, 10), 'demand': 0, 'is_depot': True}),  # noqa: E501
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
