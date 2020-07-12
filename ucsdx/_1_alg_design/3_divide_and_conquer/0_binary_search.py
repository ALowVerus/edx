# Uses python3
import sys


def binary_search(a, x):
    l, r = 0, len(a)
    while l != r and a[(l + r) // 2] != x:
        m = (l + r) // 2
        if a[m] < x:
            l = m + 1
        elif a[m] > x:
            r = m
    m = (l + r) // 2
    if m < len(a) and a[m] == x:
        return m
    return -1


if __name__ == '__main__':
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n = data[0]
    m = data[n + 1]
    a = data[1 : n + 1]
    for x in data[n + 2:]:
        # replace with the call to binary_search when implemented
        print(binary_search(a, x), end=' ')
