# Uses python3
import sys


def get_optimal_value(capacity, weights, values):
    pairs = sorted([(w, v) for w, v in zip(weights, values)], key=lambda t: t[1] / t[0], reverse=True)
    v = 0
    w = 0
    i = 0
    while i < len(pairs) and w < capacity:
        if w + pairs[i][0] <= capacity:
            v += pairs[i][1]
            w += pairs[i][0]
        else:
            v += (capacity - w) * pairs[i][1] / pairs[i][0]
            w = capacity
        i += 1
    return v


if __name__ == "__main__":
    data = list(map(int, sys.stdin.read().split()))
    n, capacity = data[0:2]
    values = data[2:(2 * n + 2):2]
    weights = data[3:(2 * n + 2):2]
    opt_value = get_optimal_value(capacity, weights, values)
    print("{:.10f}".format(opt_value))
