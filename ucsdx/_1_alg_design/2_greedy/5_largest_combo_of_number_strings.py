# Uses python3

import sys


def cmp(a, b):
    return a + b > b + a


def ms(i, k, a):
    if k - i <= 1:
        return
    j = (i + k) // 2
    ms(i, j, a)
    ms(j, k, a)
    q = []
    p0, p1 = i, j
    while p0 < j and p1 < k:
        if cmp(a[p0], a[p1]):
            q.append(a[p0])
            p0 += 1
        else:
            q.append(a[p1])
            p1 += 1
    while p0 < j:
        q.append(a[p0])
        p0 += 1
    while p1 < k:
        q.append(a[p1])
        p1 += 1
    for p in range(len(q)):
        a[i+p] = q[p]


def largest_number(a):
    ms(0, len(a), a)
    return ''.join(a)


if __name__ == '__main__':
    input = sys.stdin.read()
    data = input.split()
    a = data[1:]
    print(largest_number(a))

