# Uses python3
import sys


def lcs3_deterministic(a, b, c):
    m = [[[0 for ic in range(len(c) + 1)] for ib in range(len(b) + 1)] for ia in range(len(a) + 1)]
    for ia in range(len(a) + 1):
        for ib in range(len(b) + 1):
            for ic in range(len(c) + 1):
                if ia == 0 or ib == 0 or ic == 0:
                    m[ia][ib][ic] = 0
                elif a[ia - 1] == b[ib - 1] == c[ic - 1]:
                    m[ia][ib][ic] = m[ia - 1][ib - 1][ic - 1] + 1
                else:
                    m[ia][ib][ic] = max([m[ia - 1][ib][ic], m[ia][ib - 1][ic], m[ia][ib][ic - 1]])
    return m[len(a)][len(b)][len(c)]


def lcs3(a, b, c):
    return lcs3_deterministic(a, b, c)


if __name__ == '__main__':
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    an = data[0]
    data = data[1:]
    a = data[:an]
    data = data[an:]
    bn = data[0]
    data = data[1:]
    b = data[:bn]
    data = data[bn:]
    cn = data[0]
    data = data[1:]
    c = data[:cn]
    print(lcs3(a, b, c))
