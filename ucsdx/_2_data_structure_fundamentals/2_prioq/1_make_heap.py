# python3
from heapq import heapify, heappop
from copy import deepcopy


def build_heap(data):
    """Build a heap from ``data`` inplace.

    Returns a sequence of swaps performed by the algorithm.
    """
    # Get a heapified version of the data, without killing the original ordering
    h = deepcopy(data)
    heapify(h)
    # Relabel the items in data, such that their values are the indices they should occupy
    n_to_i = {h[i]: i for i in range(len(data))}
    data = [n_to_i[n] for n in data]
    locs = {data[i]: i for i in range(len(data))}
    # Get a heapified version of the data, without killing the original ordering
    h = deepcopy(data)
    heapify(h)
    swaps = []
    for i in range(len(data)):
        vj = heappop(h)
        if data[i] != vj:
            vi = data[i]
            j = locs[vj]
            data[i], data[j], locs[vi], locs[vj] = data[j], data[i], locs[vj], locs[vi]
            swaps.append((i, j))
    return swaps


def main():
    n = int(input())
    data = list(map(int, input().split()))
    assert len(data) == n

    swaps = build_heap(data)

    print(len(swaps))
    for i, j in swaps:
        print(i, j)


if __name__ == "__main__":
    main()
