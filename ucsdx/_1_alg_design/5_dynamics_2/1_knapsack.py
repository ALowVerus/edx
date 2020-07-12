# Uses python3
import sys


def optimal_weight(weight_total, items):
    # Sort large to small
    items = sorted(items)[::-1]
    # Recurse over the possibilities
    res = {}
    def recurse(i, w):
        if w == 0 or i >= len(items):
            res[(i, w)] = 0
        elif (i, w) not in res:
            res[(i, w)] = recurse(i+1, w)
            if w-items[i] >= 0:
                res[(i, w)] = max([res[(i, w)], recurse(i+1, w-items[i]) + items[i]])
        return res[(i, w)]
    # Call the function
    return recurse(0, weight_total)


# tests = [
#     [10, [1, 4, 8]],
#     [15, [7, 4, 8]],
#     [20, [1, 2, 3, 4, 5, 6]]
# ]
# for w, l in tests:
#     print(w, l, optimal_weight(w, l))


if __name__ == '__main__':
    input = sys.stdin.read()
    weight_total, item_count, *items = list(map(int, input.split()))
    print(optimal_weight(weight_total, items))
