# Dynamic Array

A **dynamic array** (a.k.a. array list, `Vector`, Python's `list`) is a contiguous
block of memory that grows and shrinks as elements are added and removed. It gives
you O(1) indexed access like a fixed array, plus amortised O(1) append.

`dynamic_array.py` implements one as `List[T]`.

## How it works

The class holds three things:

| field      | meaning                                             |
|------------|----------------------------------------------------|
| `data`     | the backing fixed size list; unused slots are `None` |
| `size`     | number of live elements (`0 .. capacity`)           |
| `capacity` | length of `data`, i.e. how many elements fit before a resize |

Only `data[0 : size]` is meaningful; everything from `size` onward is spare room.
When `size` reaches `capacity`, `append` allocates a new backing list
`growth_factor` times larger and copies the elements over. When the array drains
to a quarter full, `pop` halves the backing list.

### Why grow by a *factor*, not a fixed amount

Growing by 2x makes each resize twice as rare as the last, so the total copying
cost across `n` appends is `n + n/2 + n/4 + ... < 2n` — **amortised O(1)** per
append. Growing by a fixed `+k` would force a resize every `k` appends and cost
O(n) per append on average.

### Why shrink at ¼, not ½

Halving as soon as the array is half empty means an `append / pop / append / pop`
sequence right on the boundary resizes every single call. Waiting until it's only
a quarter full leaves half the buffer free after each shrink, so many operations
must pass before the next resize — keeping `pop` amortised O(1).

## Time complexity

| operation              | cost            | notes                                              |
|------------------------|-----------------|----------------------------------------------------|
| `lst[i]` / `lst[i] = x`| O(1)            | direct index into `data`                           |
| `append`               | O(1) amortised  | O(n) on the resize step, rare enough to average out |
| `pop` | O(1) amortised  | O(n) on the shrink step                            |
| `del lst[i]`           | O(n)            | shift every element after `i` left by one          |
| `x in lst` / iteration | O(n)            | linear scan of the live region                     |
| `len(lst)`             | O(1)            | returns `size`                                     |
| `==`                   | O(n)            | element-by-element                                 |

Space: O(n), with up to `~2n` allocated between resizes.

## API

```python
lst = List()  # empty, default capacity 4
lst = List(capacity=64, growth_factor=2)

lst.append(3)
lst.pop()  # -> 3 (last element); raises IndexError when empty

lst[0]  # indexed get; supports negative indices
lst[0] = 9  # indexed set
del lst[0]  # remove + shift left

len(lst)  # live element count
3 in lst  # membership scan
list(lst)  # iterate live elements only
repr(lst)  # 'List([9, 1, 2])'
lst == List()  # value equality, capacity-independent
bool(lst)  # False when empty
```

Out-of-range indices raise `IndexError`. Defining `__eq__` makes instances
unhashable, same as the built-in `list`.

## Extensions

- `insert(i, x)` / `remove(x)` / `index(x)`
- slice support in `__getitem__` / `__setitem__`
- `__add__` / `__iadd__` / `__mul__`
- iterator-invalidation check (mutation during iteration)
