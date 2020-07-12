# Uses python3


# Get the last digit of a sum of n fibonacci numbers
def fibonacci_partial_sum_last_digit(m, n):
    m %= 60
    n %= 60
    if m > n:
        n += 60
    res = {0: 0, 1: 1}
    for i in range(2, n+1):
        res[i] = (res[i - 1] + res[i - 2]) % 10
    return sum([res[i] for i in range(m, n+1)]) % 10


import sys
if __name__ == '__main__':
    input = sys.stdin.read()
    from_, to = map(int, input.split())
    print(fibonacci_partial_sum_last_digit(from_, to))