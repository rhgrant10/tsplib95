import pytest

from tsplib95 import utils


@pytest.mark.parametrize('items,kw,result,exc', [
    ([], {}, '', None),
    (list('abc'), {}, 'a, b, and c', None),
    (list('abc'), {'limit': 3}, 'a, b, and c', None),
    (list('a'), {'limit': 3}, 'a', None),
    (list('ab'), {'limit': 3}, 'a and b', None),
    (list('abcd'), {'limit': 3}, 'a, b, c, and 1 more', None),
    (list('abcde'), {'limit': 3}, 'a, b, c, and 2 more', None),
])
def test_friendly_join(items, kw, result, exc):
    if exc is not None:
        with pytest.raises(exc):
            utils.friendly_join(items, **kw)
    else:
        assert utils.friendly_join(items, **kw) == result
