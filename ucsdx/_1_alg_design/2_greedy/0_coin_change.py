# Uses python3
import sys


def get_change(m):
    n = 0
    for k in [10, 5, 1]:
        n += m // k
        m %= k
    return n


if __name__ == '__main__':
    m = int(sys.stdin.read())
    print(get_change(m))
