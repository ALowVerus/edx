# Uses python3


# Get the last digit of a sum of n fibonacci numbers
def fibonacci_sum_last_digit(n):
    # The Pisano period of 10 is 60. Get the first 60 digits
    n += 1
    n %= 60
    res = {0: 0, 1: 1}
    for i in range(2, n+1):
        res[i] = (res[i - 1] + res[i - 2]) % 10
    return sum([res[i] for i in range(n)]) % 10


import sys
if __name__ == '__main__':
    input = sys.stdin.read()
    n = int(input)
    print(fibonacci_sum_last_digit(n))
