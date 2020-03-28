import pytest

from tsplib95 import fields


@pytest.fixture
def edge_list_field():
    return fields.EdgeListField('foo')


def test_parse(edge_list_field):
    assert edge_list_field.parse('1 2\n3 4\n-1') == [[1, 2], [3, 4]]


def test_render(edge_list_field):
    assert edge_list_field.render([(1, 2), (3, 4)]) == '1 2\n3 4\n-1'
