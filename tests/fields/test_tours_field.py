import pytest

from tsplib95 import fields as F
from tsplib95 import exceptions as E


@pytest.fixture
def field():
    return F.ToursField('foo')


@pytest.mark.parametrize('text,value,exc', [
    ('', [], None),
    ('-1', [], None),
    ('-1 -1', [], None),
    ('-1 -1 -1', [], None),
    ('7 8 9', [[7, 8, 9]], None),
    ('7 8 9 -1', [[7, 8, 9]], None),
    ('7 8 9 -1 -1', [[7, 8, 9]], None),
    ('7 8 9 -1 7 8 9', [[7, 8, 9], [7, 8, 9]], None),
    ('7 8 9 -1 7 8 9 -1', [[7, 8, 9], [7, 8, 9]], None),
    ('7 8 9 -1 7 8 9 -1 -1', [[7, 8, 9], [7, 8, 9]], None),
    ('7 a 9 -1 -1', None, E.ParsingError),
])
def test_parse_with_no_terminal_required(field, text, value, exc):
    field.require_terminal = False
    if exc:
        with pytest.raises(exc):
            field.parse(text)
    else:
        field.parse(text) == value


@pytest.mark.parametrize('text,value,exc', [
    ('', [], None),
    ('-1', [], None),
    ('-1 -1', [], None),
    ('-1 -1 -1', [], None),
    ('7 8 9', None, E.ParsingError),
    ('7 8 9 -1', [[7, 8, 9]], None),
    ('7 8 9 -1 -1', [[7, 8, 9]], None),
    ('7 8 9 -1 7 8 9', None, E.ParsingError),
    ('7 8 9 -1 7 8 9 -1', [[7, 8, 9], [7, 8, 9]], None),
    ('7 8 9 -1 7 8 9 -1 -1', [[7, 8, 9], [7, 8, 9]], None),
    ('7 a 9 -1 -1', None, E.ParsingError),
])
def test_parse_with_terminal_required(field, text, value, exc):
    if exc:
        with pytest.raises(exc):
            field.parse(text)
    else:
        field.parse(text) == value


@pytest.mark.parametrize('value,text', [
    ([], ''),
    ([[]], ''),
    ([[7, 8, 9]], '7 8 9 -1\n-1'),
    ([[7, 8, 9], [7, 8, 9]], '7 8 9 -1\n7 8 9 -1\n-1'),
])
def test_render(field, value, text):
    assert field.render(value) == text
