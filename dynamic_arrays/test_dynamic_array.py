import pytest
from dynamic_array import List


def build(values, **kwargs):
    lst = List(**kwargs)
    for v in values:
        lst.append(v)
    return lst


def test_append_grows_and_preserves_order():
    lst = build(range(10), capacity=2)
    assert len(lst) == 10
    assert [lst[i] for i in range(10)] == list(range(10))


def test_capacity_grows_geometrically():
    lst = List(capacity=2, growth_factor=2)
    for v in range(5):
        lst.append(v)
    # 2 -> 4 -> 8 after crossing each boundary
    assert lst.capacity == 8


def test_getitem_negative_index():
    lst = build([10, 20, 30])
    assert lst[-1] == 30
    assert lst[-3] == 10


@pytest.mark.parametrize("bad", [3, 4, 100, -4, -100])
def test_getitem_out_of_range_raises(bad):
    lst = build([1, 2, 3])
    with pytest.raises(IndexError):
        lst[bad]


def test_getitem_on_empty_raises():
    with pytest.raises(IndexError):
        List()[0]


def test_setitem_overwrites():
    lst = build([1, 2, 3])
    lst[1] = 99
    assert lst[1] == 99
    assert len(lst) == 3


def test_setitem_negative_index():
    lst = build([1, 2, 3])
    lst[-1] = 99
    assert lst[2] == 99


def test_setitem_out_of_range_raises():
    lst = build([1, 2, 3])
    with pytest.raises(IndexError):
        lst[3] = 0


def test_delitem_middle_shifts_left():
    lst = build([0, 1, 2, 3, 4])
    del lst[1]
    assert list(lst) == [0, 2, 3, 4]
    assert len(lst) == 4


def test_delitem_last():
    lst = build([0, 1, 2])
    del lst[-1]
    assert list(lst) == [0, 1]


def test_delitem_first_repeatedly_drains():
    lst = build([0, 1, 2, 3])
    for _ in range(4):
        del lst[0]
    assert list(lst) == []
    assert len(lst) == 0


def test_delitem_out_of_range_raises():
    lst = build([1, 2, 3])
    with pytest.raises(IndexError):
        del lst[5]


def test_delitem_releases_reference():
    lst = build([1, 2, 3])
    del lst[0]
    assert lst.data[lst.size] is None


def test_iter_yields_only_live_region():
    lst = build([1, 2, 3], capacity=10)
    assert list(lst) == [1, 2, 3]


def test_iter_empty():
    assert list(List()) == []


def test_iter_is_reusable():
    lst = build([1, 2, 3])
    assert list(lst) == [1, 2, 3]
    assert list(lst) == [1, 2, 3]


def test_contains_true_and_false():
    lst = build([1, 2, 3])
    assert 2 in lst
    assert 4 not in lst


def test_contains_does_not_match_filler():
    lst = build([1, 2, 3], capacity=10)
    assert None not in lst
    assert 0 not in lst


def test_contains_cross_type_is_false_not_error():
    lst = build([1, 2, 3])
    assert "hi" not in lst


def test_repr_roundtrips_shape():
    assert repr(build([1, 2, 3])) == "List([1, 2, 3])"
    assert repr(List()) == "List([])"


def test_repr_uses_element_repr():
    assert repr(build(["a", "b"])) == "List(['a', 'b'])"


def test_eq_same_contents():
    assert build([1, 2, 3]) == build([1, 2, 3])


def test_eq_different_length():
    assert build([1, 2, 3]) != build([1, 2])


def test_eq_same_length_different_contents():
    assert build([1, 2, 3]) != build([1, 2, 4])


def test_eq_ignores_capacity():
    assert build([1, 2, 3], capacity=2) == build([1, 2, 3], capacity=64)


def test_eq_other_type_is_not_equal():
    assert build([1, 2, 3]) != [1, 2, 3]


def test_instances_are_unhashable():
    with pytest.raises(TypeError):
        {build([1, 2, 3])}


def test_bool_empty_is_false():
    assert not List()


def test_bool_nonempty_is_true():
    assert build([0])  # element is falsy, container is not


def test_bool_false_after_draining():
    lst = build([1])
    lst.pop()
    assert not lst


def test_pop_returns_last_and_shrinks_len():
    lst = build([1, 2, 3])
    assert lst.pop() == 3
    assert len(lst) == 2
    assert list(lst) == [1, 2]


def test_pop_empty_raises():
    with pytest.raises(IndexError):
        List().pop()


def test_pop_until_empty_then_raises():
    lst = build([1])
    lst.pop()
    with pytest.raises(IndexError):
        lst.pop()


def test_pop_releases_reference():
    lst = build([1, 2, 3])
    lst.pop()
    assert lst.data[lst.size] is None


def test_append_after_pop_reuses_slot():
    lst = build([1, 2, 3])
    lst.pop()
    lst.append(99)
    assert list(lst) == [1, 2, 99]


def test_shrinks_when_quarter_full():
    lst = build(range(64), capacity=4)
    cap_at_peak = lst.capacity
    for _ in range(56):
        lst.pop()
    assert lst.capacity < cap_at_peak
    assert lst.capacity >= lst.size


def test_shrink_never_below_size():
    lst = build(range(100), capacity=1)
    while len(lst):
        lst.pop()
        assert lst.capacity >= lst.size
        assert lst.capacity >= 1


def test_data_survives_grow_shrink_cycles():
    lst = List(capacity=1)
    for cycle in range(5):
        for v in range(50):
            lst.append(v)
        for _ in range(48):
            lst.pop()
    assert list(lst)[:2] == [0, 1]


@pytest.mark.parametrize("cap", [0, 1, -5])
def test_small_or_bad_capacity_still_works(cap):
    lst = List(capacity=cap)
    for v in range(10):
        lst.append(v)
    assert list(lst) == list(range(10))


def test_growth_factor_three():
    lst = List(capacity=2, growth_factor=3)
    for v in range(3):
        lst.append(v)
    assert lst.capacity == 6
    assert list(lst) == [0, 1, 2]
