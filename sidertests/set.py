from attest import Tests, assert_hook, raises
from .env import get_session, key
from sider.types import Set, Integer


tests = Tests()

S = frozenset
IntSet = Set(Integer)


@tests.test
def iterate():
    session = get_session()
    set_ = session.set(key('test_set_iterate'), S('abc'), Set)
    assert S(['a', 'b', 'c']) == S(set_)
    setx = session.set(key('test_setx_iterate'), S([1, 2, 3]), Set(Integer))
    assert S([1, 2, 3]) == S(setx)


@tests.test
def length():
    session = get_session()
    set_ = session.set(key('test_set_length'), S('abc'), Set)
    assert len(set_) == 3
    setx = session.set(key('test_setx_length'), S([1, 2, 3]), Set(Integer))
    assert len(setx) == 3


@tests.test
def contains():
    session = get_session()
    set_ = session.set(key('test_set_contains'), S('abc'), Set)
    assert 'a' in set_
    assert 'd' not in set_
    setx = session.set(key('test_setx_contains'), S([1, 2, 3]), Set(Integer))
    assert 1 in setx
    assert 4 not in setx
    assert '1' not in setx
    assert '4' not in setx


@tests.test
def equals():
    session = get_session()
    set_ = session.set(key('test_set_equals'), S('abc'), Set)
    assert set_ == set('abc')
    assert set_ == S('abc')


@tests.test
def isdisjoint():
    session = get_session()
    set_ = session.set(key('test_set_isdisjoint'), S('abc'), Set)
    setj = session.set(key('test_set_isdisjoint2'), S('cde'), Set)
    setd = session.set(key('test_set_isdisjoint3'), S('def1'), Set)
    assert not set_.isdisjoint('cde')
    assert set_.isdisjoint('def')
    assert not set_.isdisjoint(S('cde'))
    assert set_.isdisjoint(S('def'))
    assert not set_.isdisjoint(setj)
    assert set_.isdisjoint(setd)
    assert not setj.isdisjoint(set_)
    assert setd.isdisjoint(set_)
    setx = session.set(key('test_setx_isdisjoint'), S([1, 2, 3]), IntSet)
    setxj = session.set(key('test_setx_isdisjoint2'), S([3, 4, 5]), IntSet)
    setxd = session.set(key('test_setx_isdisjoint3'), S([4, 5, 6]), IntSet)
    assert not setx.isdisjoint([3, 4, 5])
    assert setx.isdisjoint([4, 5, 6])
    assert not setx.isdisjoint(S([3, 4, 5]))
    assert setx.isdisjoint(S([4, 5, 6]))
    assert not setx.isdisjoint(setxj)
    assert setx.isdisjoint(setxd)
    assert not setxj.isdisjoint(setx)
    assert setxd.isdisjoint(setx)
    # mismatched value_type Integer vs. Bulk:
    assert setd.isdisjoint(setx)
    assert setx.isdisjoint(setd)
    assert setd.isdisjoint(setxj)
    assert setd.isdisjoint(setxd)
    assert setxj.isdisjoint(setd)
    assert setxd.isdisjoint(setd)


@tests.test
def difference():
    session = get_session()
    set_ = session.set(key('test_set_difference'), S('abcd'), Set)
    set2 = session.set(key('test_set_difference2'), S('bde1'), Set)
    assert set_.difference(set2) == S('ac')
    assert set_.difference('bdef') == S('ac')
    assert set_.difference(S('bdef')) == S('ac')
    assert set_ - set2 == S('ac')
    assert set_ - S('bdef') == S('ac')
    with raises(TypeError):
        set_ - 'bdef'
    setx = session.set(key('test_setx_difference'), S([1, 2, 3, 4]), IntSet)
    sety = session.set(key('test_setx_difference2'), S([2, 4, 5, 6]), IntSet)
    assert setx.difference(sety) == S([1, 3])
    assert setx.difference([2, 4, 5, 6]) == S([1, 3])
    assert setx.difference(S([2, 4, 5, 6])) == S([1, 3])
    assert setx - sety == S([1, 3])
    assert setx - S([2, 4, 5, 6]) == S([1, 3])
    with raises(TypeError):
        setx - [2, 4, 5, 6]
    # mismatched value_type Integer vs. Bulk:
    assert set2 == set2.difference(setx)
    assert setx == setx.difference(set2)


@tests.test
def union():
    session = get_session()
    set_ = session.set(key('test_set_union'), S('abc'), Set)
    set2 = session.set(key('test_set_union2'), S('cde'), Set)
    set3 = session.set(key('test_set_union3'), S('def'), Set)
    assert set_.union('cde') == S('abcde')
    assert set_.union('cde', 'def') == S('abcdef')
    assert set_.union(S('cde')) == S('abcde')
    assert set_.union(S('cde'), 'def') == S('abcdef')
    assert set_.union(S('cde'), S('def')) == S('abcdef')
    assert set_.union(set2) == S('abcde')
    assert set_.union(set2, set3) == S('abcdef')
    assert set_.union(set2, set3, 'adfg') == S('abcdefg')
    assert set_ | S('cde') == S('abcde')
    assert set_ | set2 == S('abcde')
    with raises(TypeError):
        set_ | 'cde'
    setx = session.set(key('test_setx_union'), S([1, 2, 3]), IntSet)
    sety = session.set(key('test_setx_union2'), S([3, 4, 5]), IntSet)
    setz = session.set(key('test_setx_union3'), S([4, 5, 6]), IntSet)
    assert setx.union([3, 4, 5]) == S([1, 2, 3, 4, 5])
    assert setx.union([3, 4, 5], [4, 5, 6]) == S([1, 2, 3, 4, 5, 6])
    assert setx.union(S([3, 4, 5])) == S([1, 2, 3, 4, 5])
    assert setx.union(S([3, 4, 5]), [4, 5, 6]) == S([1, 2, 3, 4, 5, 6])
    assert setx.union(S([3, 4, 5]), S([4, 5, 6])) == S([1, 2, 3, 4, 5, 6])
    assert setx.union(sety) == S([1, 2, 3, 4, 5])
    assert setx.union(sety, setz) == S([1, 2, 3, 4, 5, 6])
    assert setx.union(sety, setz, [1, 4, 6, 7]) == S([1, 2, 3, 4, 5, 6, 7])
    assert setx | S([3, 4, 5]) == S([1, 2, 3, 4, 5])
    assert setx | sety == S([1, 2, 3, 4, 5])
    with raises(TypeError):
        setx | [3, 4, 5]
    assert set_.union(setx) == S(['a', 'b', 'c', 1, 2, 3])
    assert set_.union(setx, sety) == S(['a', 'b', 'c', 1, 2, 3, 4, 5])
    assert (set_.union(set2, setx, sety)
            == S(['a', 'b', 'c', 'd', 'e', 1, 2, 3, 4, 5]))
    assert set_ | setx == S(['a', 'b', 'c', 1, 2, 3])
