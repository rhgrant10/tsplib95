import pytest
import textwrap

from tsplib95 import fields


@pytest.fixture
def f():
    return fields.MatrixField('foo')


def test_field_parse(f):
    text = textwrap.dedent('''
        0 0 0
        1 3 4
        2 -1 5
    ''')
    assert f.parse(text) == [
        [0, 0.0, 0.0],
        [1, 3.0, 4.0],
        [2, -1.0, 5.0],
    ]


def test_field_render(f):
    value = [
        [0, 0.0, 0.0],
        [1, 3.0, 4.0],
        [2, -1.0, 5.0],
    ]
    assert f.render(value) == textwrap.dedent('''
        0 0.0 0.0
        1 3.0 4.0
        2 -1.0 5.0
    ''').strip()


@pytest.fixture
def value(request):
    return {
        2: {
            0: [0.0, 0.0],
            1: [3.0, 4.0],
            2: [-1.0, 0.5],
        },
        3: {
            0: [0.0, 0.0, 0.0],
            1: [3.0, 4.0, 5.0],
            2: [-1.0, 0.5, 2.0],
        },
        (2, 3): {
            0: [0.0, 0.0],
            1: [3.0, 4.0, 5.0],
            2: [-1.0, 0.5],
        }
    }[request.param]
