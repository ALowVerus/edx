# Uses python3
import sys


def optimal_summands(n):
    summands = []
    c = 1
    while n >= c:
        n -= c
        summands.append(c)
        c += 1
    for i in range(n):
        summands[-i-1] += 1
    # write your code here
    return summands


if __name__ == '__main__':
    input = sys.stdin.read()
    n = int(input)
    summands = optimal_summands(n)
    print(len(summands))
    for x in summands:
        print(x, end=' ')
