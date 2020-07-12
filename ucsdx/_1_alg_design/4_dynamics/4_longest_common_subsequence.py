# Uses python3
import sys


def lcs_deterministic(a, b):
    m = [[0 for ib in range(len(b) + 1)] for ia in range(len(a) + 1)]
    for ia in range(len(a) + 1):
        for ib in range(len(b) + 1):
            if ia == 0 or ib == 0:
                m[ia][ib] = 0
            elif a[ia - 1] == b[ib - 1]:
                m[ia][ib] = m[ia - 1][ib - 1] + 1
            else:
                m[ia][ib] = max([m[ia - 1][ib], m[ia][ib - 1]])
    return m[len(a)][len(b)]


def lcs_recursive(a, b):
    d = {}

    def recurse(ia, ib):
        if (ia, ib) in d:
            return d[(ia, ib)]
        elif a[ia - 1] == b[ib - 1]:
            d[(ia, ib)] = recurse(ia - 1, ib - 1)
        else:
            d[(ia, ib)] = max([recurse(ia - 1, ib), recurse(ia, ib - 1)])

    recurse(len(a), len(b))
    return d[(len(a), len(b))]


def lcs2(a, b):
    return lcs_deterministic(a, b)


if __name__ == '__main__':
    input = sys.stdin.read()
    data = list(map(int, input.split()))

    n = data[0]
    data = data[1:]
    a = data[:n]

    data = data[n:]
    m = data[0]
    data = data[1:]
    b = data[:m]

    print(lcs2(a, b))
