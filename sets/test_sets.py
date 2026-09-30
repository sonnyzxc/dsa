import random
import pytest
from direct_address_set import DirectAddressSet

IMPLEMENTATIONS = [DirectAddressSet]
MAX_VALUE = 10**6 - 1


@pytest.fixture(params=IMPLEMENTATIONS, ids=lambda cls: cls.__name__)
def s(request):
    return request.param()


def test_starts_empty(s):
    assert len(s) == 0
    assert 5 not in s


def test_add_and_contains(s):
    s.add(5)
    assert 5 in s
    assert len(s) == 1


def test_add_is_idempotent(s):
    s.add(5)
    s.add(5)
    assert len(s) == 1


def test_boundaries(s):
    for x in (0, MAX_VALUE):
        s.add(x)
        assert x in s
    assert len(s) == 2


def test_discard(s):
    s.add(5)
    s.discard(5)
    assert 5 not in s
    assert len(s) == 0


def test_discard_missing_keeps_size(s):
    s.add(1)
    s.discard(2)
    assert len(s) == 1
    assert 1 in s


def test_discard_twice(s):
    s.add(5)
    s.discard(5)
    s.discard(5)
    assert len(s) == 0


def test_readd_after_discard(s):
    s.add(5)
    s.discard(5)
    s.add(5)
    assert 5 in s
    assert len(s) == 1


@pytest.mark.parametrize("seed", range(5))
def test_matches_builtin_set(s, seed):
    rng = random.Random(seed)
    pool = [0, MAX_VALUE] + [rng.randrange(MAX_VALUE) for _ in range(30)]
    ref = set()

    for _ in range(5000):
        op = rng.choice(["add", "discard", "contains"])
        x = rng.choice(pool)

        if op == "add":
            s.add(x)
            ref.add(x)
        elif op == "discard":
            s.discard(x)
            ref.discard(x)
        else:
            assert (x in s) == (x in ref)

        assert len(s) == len(ref)


class TestDirectAddressSetLimits:
    def test_add_out_of_range(self):
        s = DirectAddressSet()
        for bad in (-1, 10**6):
            with pytest.raises(ValueError):
                s.add(bad)

    def test_add_wrong_type(self):
        with pytest.raises(TypeError):
            DirectAddressSet().add("a")

    def test_contains_never_raises(self):
        s = DirectAddressSet()
        assert -1 not in s
        assert 10**6 not in s
        assert "a" not in s

    def test_discard_invalid_is_silent(self):
        s = DirectAddressSet()
        s.add(1)
        for bad in (-1, 10**6, "a", None):
            s.discard(bad)
        assert len(s) == 1
