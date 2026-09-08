from collections.abc import Iterator


class List[T]:
    def __init__(self, capacity=4, growth_factor=2) -> None:
        self.capacity = max(1, capacity)
        self.data = [None] * self.capacity
        self.size = 0
        self.growth_factor = growth_factor

    def __len__(self) -> int:
        return self.size

    def __getitem__(self, index: int) -> T:
        return self.data[self._normalize(index)]

    def __setitem__(self, index: int, value: T) -> None:
        self.data[self._normalize(index)] = value

    def __delitem__(self, index: int) -> None:
        index = self._normalize(index)
        for i in range(index, self.size - 1):
            self.data[i] = self.data[i + 1]
        self.size -= 1
        self.data[self.size] = None

    def __iter__(self) -> Iterator[T]:
        for i in range(self.size):
            yield self.data[i]

    # item is an `object` because `"hi" in list_of_ints` is well defined
    def __contains__(self, item: object) -> bool:
        return any(val == item for val in self)

    def __repr__(self) -> str:
        return f"List([{', '.join(repr(x) for x in self)}])"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, List):
            return NotImplemented
        return len(self) == len(other) and all(a == b for a, b in zip(self, other))

    def __bool__(self) -> bool:
        return self.size > 0

    def _normalize(self, index: int) -> int:
        if index < 0:
            index += self.size
        if not 0 <= index < self.size:
            raise IndexError("index out of range")
        return index

    def _resize(self, new_capacity: int) -> None:
        new_capacity = max(1, new_capacity)
        new_data = [None] * new_capacity
        for i in range(self.size):
            new_data[i] = self.data[i]
        self.data = new_data
        self.capacity = new_capacity

    def append(self, item: T) -> None:
        if self.size == self.capacity:
            self._resize(self.capacity * self.growth_factor)
        self.data[self.size] = item
        self.size += 1

    def pop(self) -> T:
        if self.size == 0:
            raise IndexError("popping from empty list")
        self.size -= 1
        data = self.data[self.size]
        self.data[self.size] = None
        if 0 < self.size <= self.capacity // 4:
            self._resize(self.capacity // 2)
        return data
