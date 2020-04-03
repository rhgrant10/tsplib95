import pytest

from tsplib95 import fields as F
from tsplib95 import exceptions as E


@pytest.fixture
def field():
    return F.EdgeDataField('foo')


@pytest.mark.parametrize('text,value,exc', [
    ('1 2\n2 3\n-1', [(1, 2), (2, 3)], None),
    ('1 2\n2 x\n-1', [(1, 2), (2, 3)], E.ParsingError),
    ('1 2 3\n2 3\n-1', {1: [2, 3], 2: [3]}, None),
    ('1 x 3\n2 3\n-1', {1: [2, 3], 2: [3]}, E.ParsingError),
])
def test_parse(field, text, value, exc):
    if exc:
        with pytest.raises(exc):
            field.parse(text)
    else:
        field.parse(text) == value
