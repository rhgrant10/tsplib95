import pytest

from tsplib95 import transformers as T


@pytest.fixture
def tf():
    return T.Transformer()


@pytest.mark.parametrize('text,value', [
    ('foo', 'foo'),
    (None, None),
    (0, 0),
    (3.14, 3.14),
])
def test_transformer_parse(tf, text, value):
    assert tf.parse(text) == value


@pytest.mark.parametrize('value,text', [
    ('foo', 'foo'),
    (None, ''),
    (0, '0'),
    (3.14, '3.14'),
])
def test_transformer_render(tf, value, text):
    assert tf.render(value) == text


def test_transformer_validate(tf):
    anything = object()
    assert tf.validate(anything) is None
