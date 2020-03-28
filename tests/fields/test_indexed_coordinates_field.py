import pytest
import textwrap

from tsplib95 import exceptions
from tsplib95 import fields


def test_field_parse():
    f = fields.IndexedCoordinatesField('foo')
    text = textwrap.dedent('''
        0 0 0
        1 3 4
        2 -1 0.5
    ''')
    assert f.parse(text) == {
        0: [0.0, 0.0],
        1: [3.0, 4.0],
        2: [-1.0, 0.5],
    }


def test_field_render():
    f = fields.IndexedCoordinatesField('foo')
    value = {
        0: [0.0, 0.0],
        1: [3.0, 4.0],
        2: [-1.0, 0.5],
    }
    assert f.render(value) == textwrap.dedent('''
        0 0.0 0.0
        1 3.0 4.0
        2 -1.0 0.5
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


@pytest.mark.parametrize('value,dimensions,error', [
    (2, None, None),
    (2, 2, None),
    (2, 3, exceptions.ValidationError),
    (2, (2, 3), None),
    (3, None, None),
    (3, 2, exceptions.ValidationError),
    (3, 3, None),
    (3, (2, 3), None),
    ((2, 3), None, None),
    ((2, 3), 2, exceptions.ValidationError),
    ((2, 3), 3, exceptions.ValidationError),
    ((2, 3), (2, 3), exceptions.ValidationError),
], indirect=['value'])
def test_dimensionality_validation(value, dimensions, error):
    f = fields.IndexedCoordinatesField('foo', dimensions=dimensions)
    if error is None:
        assert f.validate(value) is None
    else:
        with pytest.raises(error):
            f.validate(value)
