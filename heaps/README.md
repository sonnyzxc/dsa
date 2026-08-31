# Heap

A **heap** is a complete binary tree that satisfies the *heap invariant*:

- **min-heap**: every parent `<=` both of its children (smallest value at the root)
- **max-heap**: every parent `>=` both of its children (largest value at the root)

"Complete" means every level is full except possibly the last, which fills left to
right. That regularity lets the tree live in a flat array with no pointers.

`heap.py` implements a **min-heap**.

## Array representation

The tree is stored breadth-first in `self.data`. For the node at index `i`:

| relation    | index          |
|-------------|----------------|
| parent      | `(i - 1) // 2` |
| left child  | `2i + 1`       |
| right child | `2i + 2`       |

```
index:  0   1   2   3   4   5   6
        0
       / \
      1   2
     / \ / \
    3  4 5  6
```

## Operations

| op           | cost      | how it works                                                        |
|--------------|-----------|--------------------------------------------------------------------|
| peek min     | O(1)      | it's always `data[0]`                                              |
| `push`       | O(log n)  | append at the end, then **sift up** while smaller than its parent  |
| `pop`        | O(log n)  | take `data[0]`, move the last element to the root, then **sift down** while larger than its smaller child |
| `heapify`    | O(n)      | sift down every internal node, from the last one back to the root  |

`heapify` is O(n), not O(n log n): most nodes are near the bottom and barely move,
and the work forms a converging series. Building by repeated `push` would be
O(n log n).

**Sift up / sift down** are the two
repair routines that walk a single root-to-leaf path restoring the invariant.

## API

```python
h = Heap()                # empty
h = Heap([5, 3, 8, 1])    # heapified in O(n)

h.push(4)
h.pop()                   # -> 1  (smallest); raises EmptyHeapError when empty
h[0]                      # peek minimum
len(h)
repr(h)                   # 'Heap([1, 3, 8, 5])'
```

## Extensions

- max-heap / custom comparator (`key=`)
- fixed capacity (bounded heap)
- pretty-print the tree
