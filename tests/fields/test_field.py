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
    with pytest.raises(NotImplementedError):
        field.render(42)


def test_field_parse(field):
    with pytest.raises(NotImplementedError):
        field.parse('42')


def test_field_validate(field):
    assert field.validate(42) is None
