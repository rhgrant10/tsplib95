import pytest

from tsplib95 import fields as F
from tsplib95 import exceptions as E


@pytest.fixture
def field():
    return F.DemandsField('foo')


@pytest.mark.parametrize('text,value,exc', [
    ('1 2', {1: 2}, None),
    ('1 2\n2 3', {1: 2, 2: 3}, None),
    ('2 x 0', None, E.ParsingError),
])
def test_parse(field, text, value, exc):
    if exc:
        with pytest.raises(exc):
            field.parse(text)
    else:
        field.parse(text) == value
