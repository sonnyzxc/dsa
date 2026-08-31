
# Heap
> specialised binary tree that satisfies the heap invariant

max-heap: every parent node is greater than or equal to both of its children
min-heap: every parent node is less than or equal to both of its children

guarentees:
- maximum/minimum lookup is O(1)
- insert new element or remove in O(logn)

    0
   / \
  1   2
 / \ / \
3  4 5  6

extensions:
- min, max custom
- custom comparator
- fixed size
- print tree (repr)
