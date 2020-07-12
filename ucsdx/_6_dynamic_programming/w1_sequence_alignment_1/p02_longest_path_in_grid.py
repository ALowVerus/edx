# python3
import sys


def longest_path(n, m, down, right):
    # TODO: your code here
    history = [[0 for col in range(m+1)] for row in range(n+1)]
    for row in range(n+1):
        for col in range(m+1):
            options = [0]
            if row > 0:
                options.append(history[row - 1][col] + down[row - 1][col])
            if col > 0:
                options.append(history[row][col - 1] + right[row][col - 1])
            history[row][col] = max(options)
    return history[-1][-1]


if __name__ == "__main__":
    n, m = map(int, sys.stdin.readline().strip().split())
    down = [list(map(int, sys.stdin.readline().strip().split()))
            for _ in range(n)]
    sys.stdin.readline()
    right = [list(map(int, sys.stdin.readline().strip().split()))
             for _ in range(n + 1)]

    print(longest_path(n, m, down, right))
