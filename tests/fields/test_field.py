import pytest

from tsplib95 import fields


@pytest.fixture
def field():
    return fields.Field('foo')


def test_field_requires_name():
    with pytest.raises(TypeError):
        fields.Field()


def test_field_name(field):
    assert field.keyword == 'foo'


def test_field_render(field):
    assert field.render(42) == '42'


def test_field_parse(field):
    assert field.parse('bar 42') == 'bar 42'


def test_field_validate(field):
    assert field.validate(42) is None
