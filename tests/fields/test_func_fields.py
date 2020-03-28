import pytest

from tsplib95 import fields


cases = [
    (fields.IntegerField, '42', 42),
    (fields.FloatField, '3.14', 3.14),
    (fields.NumberField, '42', 42),
    (fields.NumberField, '3.14', 3.14),
    (fields.StringField, 'hello', 'hello'),
]


@pytest.mark.parametrize('field,text,value', cases)
def test_func_field_parse(field, text, value):
    assert field('foo').parse(text) == value


@pytest.mark.parametrize('field,text,value', cases)
def test_func_field_render(field, text, value):
    assert field('foo').render(value) == text
