import pytest

from tsplib95 import fields as F
from tsplib95 import exceptions as E


@pytest.fixture
def field():
    return F.DepotsField('foo')


@pytest.mark.parametrize('text,value,exc', [
    ('1\n2 -1', [1, 2], None),
    ('1 2 -1', [1, 2], None),
    ('1 2 3 -1', [1, 2, 3], None),
    ('-1', [], None),
    ('1 x 2 -1', [], E.ParsingError),
    ('1- 2 -1', [], E.ParsingError),
    ('', [], E.ParsingError),
])
def test_parse(field, text, value, exc):
    if exc:
        with pytest.raises(exc):
            field.parse(text)
    else:
        field.parse(text) == value
