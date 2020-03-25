import pytest

from tsplib95.v2 import fields


@pytest.fixture
def field():
    return fields.Field(name='foo')


def test_field_requires_name():
    with pytest.raises(TypeError):
        fields.Field()


def test_field_name(field):
    assert field.name == 'foo'


def test_field_render(field):
    assert field.render(42) == '42'


def test_field_parse(field):
    assert field.parse('foo 42') == 'foo 42'


def test_field_validate(field):
    assert field.validate(42) is None
