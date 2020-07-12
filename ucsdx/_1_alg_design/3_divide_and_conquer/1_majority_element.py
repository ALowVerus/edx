# Uses python3
import sys
from collections import Counter


def get_majority_element(a):
    return [-1, 1][Counter(a).most_common(1)[0][1] > len(a) // 2]


if __name__ == '__main__':
    input = sys.stdin.read()
    n, *a = list(map(int, input.split()))
    if get_majority_element(a) != -1:
        print(1)
    else:
        print(0)
