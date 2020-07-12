# Uses python3
import sys


def triple_knapsack(items):
    item_sum = sum(items)
    if item_sum % 3 != 0:
        return False
    items = sorted(items, reverse=True)
    # Recurse over the possibilities
    res = {}
    def recurse(i, weights):
        if sum(weights) == 0:
            return 1
        elif i >= len(items):
            return 0
        elif (i, weights) not in res:
            res[(i, weights)] = recurse(i+1, weights)
            for wi in range(3):
                if weights[wi]-items[i] >= 0:
                    temp_weights = [w for w in weights]
                    temp_weights[wi] -= items[i]
                    res[(i, weights)] = max([res[(i, weights)], recurse(i+1, tuple(temp_weights))])
        return res[(i, weights)]
    # Call the function
    return recurse(0, (item_sum // 3, item_sum // 3, item_sum // 3))


if __name__ == '__main__':
    input = sys.stdin.read()
    n, *A = list(map(int, input.split()))
    print(int(triple_knapsack(A)))
