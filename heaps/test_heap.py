import pytest  # noqa: F401

from heap import EmptyHeapError, Heap

def test_heap_property():
    h = Heap()
    for v in [5, 3, 8, 1, 9, 2, 7, 0]:
        h.push(v)
    for i in range(len(h)):
        for c in (2*i + 1, 2*i + 2):
            if c < len(h):
                assert h[i] <= h[c], f"{d[i]} at {i} > child {h[c]} at {c}"

def test():
    h = Heap()
    for v in [3, 2, 1, 0]:
        h.push(v)
    assert h.pop() == 0
    assert h.pop() == 1
    assert h.pop() == 2
    assert h.pop() == 3

def is_min_heap(d) -> bool:
    return all(
        d[i] <= d[c]
        for i in range(len(d))
        for c in (2*i + 1, 2*i + 2)
        if c < len(d)
    )

def test_heapify_debug():
    raw = [9, 4, 7, 1, 0, 3, 8, 2, 6, 5]
    h = Heap(raw)
    print("raw:  ", raw)
    print("heap: ", h.data)
    assert is_min_heap(h.data)
    assert sorted(h.data) == sorted(raw)
