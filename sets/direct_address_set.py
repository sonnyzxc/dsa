class DirectAddressSet:
    """Set of ints in [0, 10^6) via a flat array of flags"""

    _CAPACITY = 10**6

    def __init__(self) -> None:
        self._present = [False] * self._CAPACITY
        self._size = 0

    def __len__(self) -> int:
        return self._size

    def __contains__(self, x: object) -> bool:
        return isinstance(x, int) and 0 <= x < self._CAPACITY and self._present[x]

    def _check(self, x: int) -> None:
        if not isinstance(x, int):
            raise TypeError(f"expected int, got {type(x).__name__}")
        if not 0 <= x < self._CAPACITY:
            raise ValueError(f"{x} out of range [0, {self._CAPACITY})")

    def add(self, x: int) -> None:
        self._check(x)
        if not self._present[x]:
            self._present[x] = True
            self._size += 1

    def discard(self, x: object) -> None:
        if x in self:
            self._present[x] = False
            self._size -= 1
