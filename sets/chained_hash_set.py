from collections.abc import Hashable

"""
Known limitations:
- poor hash spread for patterned keys (use prime sizes or bit mixing)
- O(n) worst case with heavy collisions (treeify buckets)
- O(n) latency spike on resize (incremental rehashing), and no shrinking
"""

class ChainedHashSet[T: Hashable]:
    """HashSet using chaining via singly linked buckets"""

    def __init__(self, num_buckets: int = 8) -> None:
        self._buckets: list[list[T]] = [[] for _ in range(num_buckets)]
        self._size = 0

    def _bucket(self, x: object) -> list[T]:
        return self._buckets[hash(x) % len(self._buckets)]

    def __len__(self) -> int:
        return self._size

    def __contains__(self, x: object):
        return x in self._bucket(x)

    def add(self, x: T) -> None:
        bucket = self._bucket(x)
        if x not in bucket:
            bucket.append(x)
            self._size += 1
            # load factor
            if self._size > 0.75 * len(self._buckets):
                self._resize()

    def discard(self, x: T) -> None:
        bucket = self._bucket(x)
        if x in bucket:
            bucket.remove(x)
            self._size -= 1

    def _resize(self) -> None:
        old = self._buckets
        self._buckets = [[] for _ in range(2 * len(old))]
        for bucket in old:
            for x in bucket:
                self._bucket(x).append(x)
