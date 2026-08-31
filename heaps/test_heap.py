import pytest
from heap import EmptyHeapError, Heap


def assert_min_heap(d):
    for i in range(len(d)):
        for c in (2 * i + 1, 2 * i + 2):
            if c < len(d):
                assert d[i] <= d[c], f"{d[i]} at {i} > child {d[c]} at {c} in {d}"


def test_push_keeps_heap_property():
    h = Heap()
    for v in [5, 3, 8, 1, 9, 2, 7, 0]:
        h.push(v)
    assert_min_heap(h.data)


def test_pop_returns_ascending():
    h = Heap()
    for v in [3, 2, 1, 0]:
        h.push(v)
    assert [h.pop() for _ in range(4)] == list(range(4))


def test_pop_drains_in_order():
    h = Heap()
    for v in [5, 3, 8, 1, 9, 2, 7, 0, 4, 6]:
        h.push(v)
    assert [h.pop() for _ in range(10)] == list(range(10))


def test_heapify_builds_valid_heap():
    h = Heap([9, 4, 7, 1, 0, 3, 8, 2, 6, 5])
    assert_min_heap(h.data)
    assert sorted(h.data) == list(range(10))


def test_pop_empty_raises():
    with pytest.raises(EmptyHeapError):
        Heap().pop()


def test_pop_until_empty_then_raises():
    h = Heap()
    h.push(1)
    h.pop()
    with pytest.raises(EmptyHeapError):
        h.pop()
