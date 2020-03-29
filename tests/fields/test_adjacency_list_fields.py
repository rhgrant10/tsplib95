import pytest

from tsplib95 import fields


@pytest.fixture
def adj_list_field():
    return fields.AdjacencyListField('foo')


@pytest.fixture
def text():
    return '\n'.join([
        '0 1 2 3 -1',
        '1 0 2 3 -1',
        '2 0 1 3 -1',
        '3 0 1 2 -1',
        '-1',
    ])


@pytest.fixture
def edges():
    return {
        0: [1, 2, 3],
        1: [0, 2, 3],
        2: [0, 1, 3],
        3: [0, 1, 2],
    }


def test_parse(adj_list_field, text, edges):
    assert adj_list_field.parse(text) == edges


def test_render(adj_list_field, text, edges):
    assert adj_list_field.render(edges) == text
