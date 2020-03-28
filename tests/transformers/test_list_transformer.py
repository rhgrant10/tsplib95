import pytest

from tsplib95 import transformers as T


@pytest.fixture
def list_transformer():
    def make(**kwargs):
        tf = T.ListT(**kwargs)
        return tf
    return make


def test_that_it_works(list_transformer):
    text = 'foo bar baz'
    items = ['foo', 'bar', 'baz']
    tf = list_transformer()
    assert tf.parse(text) == items
    assert tf.render(items) == text


@pytest.mark.parametrize('items,container', [
    ('abc', ['a', 'b', 'c']),
    ('', []),
])
def test_list_transformer_pack(list_transformer, items, container):
    tf = list_transformer()
    assert tf.pack(items) == container


@pytest.mark.parametrize('items,container', [
    ('abc', ['a', 'b', 'c']),
    ('', []),
])
def test_list_transformer_unpack(list_transformer, items, container):
    tf = list_transformer()
    assert tf.unpack(container) == container
