import pytest
from unittest import mock

from tsplib95 import fields
from tsplib95 import exceptions


@pytest.fixture
def field():
    return fields.TransformerField('foo', transformer=mock.Mock())


def test_field_render(field):
    assert field.render(42) is field.tf.render.return_value


def test_field_render_rendering_error(field):
    field.tf.render.side_effect = exceptions.RenderingError()
    with pytest.raises(exceptions.RenderingError):
        field.render(42)


def test_field_render_exception(field):
    field.tf.render.side_effect = Exception()
    with pytest.raises(Exception):
        field.render(42)


def test_field_parse(field):
    assert field.parse('42') is field.tf.parse.return_value


def test_field_parse_parsing_error(field):
    field.tf.parse.side_effect = exceptions.ParsingError()
    with pytest.raises(exceptions.ParsingError):
        field.parse(42)


def test_field_parse_exception(field):
    field.tf.parse.side_effect = Exception()
    with pytest.raises(Exception):
        field.parse(42)


def test_field_validate(field):
    assert field.validate(42) is field.tf.validate.return_value
