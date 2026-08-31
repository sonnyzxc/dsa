class EmptyHeapError(IndexError):
    pass


class Heap[T]:
    def __init__(self, arr: list[T] | None = None) -> None:
        self.data: list[T] = list(arr) if arr else []
        self.heapify()

    def __repr__(self) -> str:
        return f"Heap({self.data})"

    def __len__(self) -> int:
        return len(self.data)

    def __getitem__(self, index: int) -> T:
        return self.data[index]

    @staticmethod
    def _parent(index: int) -> int | None:
        return (index - 1) // 2 if index > 0 else None

    @staticmethod
    def _left_child(index: int) -> int:
        return index * 2 + 1

    @staticmethod
    def _right_child(index: int) -> int:
        return index * 2 + 2

    def _swap(self, i, j) -> None:
        self.data[i], self.data[j] = self.data[j], self.data[i]

    def _sift_up(self, index: int) -> None:
        while index > 0:
            parent = self._parent(index)
            if self.data[parent] <= self.data[index]:
                break
            self._swap(parent, index)
            index = parent

    def _sift_down(self, index: int) -> None:
        left = self._left_child(index)
        while left < len(self.data):
            right = self._right_child(index)
            smaller = left
            if right < len(self.data) and self.data[right] < self.data[left]:
                smaller = right
            if self.data[index] <= self.data[smaller]:
                break
            self._swap(index, smaller)
            index = smaller
            left = self._left_child(index)

    def push(self, value) -> None:
        self.data.append(value)
        self._sift_up(len(self.data) - 1)

    def pop(self) -> T:
        if not self.data:
            raise EmptyHeapError("popping from empty heap.")
        last = self.data.pop()
        if not self.data:
            return last
        val = self.data[0]
        self.data[0] = last
        self._sift_down(0)
        return val

    def heapify(self) -> None:
        last = self._parent(len(self.data) - 1)
        if last is None:
            return
        for i in range(last, -1, -1):
            self._sift_down(i)
