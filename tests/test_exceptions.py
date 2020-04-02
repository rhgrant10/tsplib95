import pytest

from tsplib95 import exceptions


@pytest.mark.parametrize('initial,msg,final', [
    (('foo',), 'bar', ('bar: foo',)),
    (('foo', 'baz'), 'bar', ('bar: foo', 'baz')),
    (tuple(), 'bar', ('bar',)),
    ((None, 'baz'), 'bar', ('bar', 'baz')),
])
def test_exception_wrap(initial, msg, final):
    e = Exception(*initial)
    w = exceptions.TsplibError.wrap(e, msg)
    assert w.args == final


@pytest.mark.parametrize('initial,msg,final', [
    (('foo',), 'bar', ('bar: foo',)),
    (('foo', 'baz'), 'bar', ('bar: foo', 'baz')),
    (tuple(), 'bar', ('bar',)),
    ((None, 'baz'), 'bar', ('bar', 'baz')),
])
def test_exception_amend(initial, msg, final):
    e = exceptions.TsplibError(*initial).amend(msg)
    assert e.args == final
