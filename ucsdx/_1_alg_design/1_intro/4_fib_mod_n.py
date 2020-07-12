# Uses python3
import sys


def get_fibonacci_mod_m(n, m):
    # Calculate and return Pisano Period
    # The length of a Pisano Period for
    # a given m ranges from 3 to m * m
    def pisanoPeriod(n, m):
        previous, current = 0, 1
        for i in range(0, min([n, m * m])):
            previous, current = current, (previous + current) % m
            # A Pisano Period starts with 01
            if (previous == 0 and current == 1):
                return i + 1
        return None
    # Getting the period
    pisano_period = pisanoPeriod(n, m)
    print(pisano_period)

    if pisano_period is not None:
        # Taking mod of N with
        # period length
        n = n % pisano_period

    previous, current = 0, 1
    if n == 0:
        return 0
    elif n == 1:
        return 1
    for i in range(n - 1):
        previous, current = current, previous + current

    return current % m


if __name__ == '__main__':
    input = input("Enter 2 digits: ")
    n, m = map(int, input.split())
    print(n, m)
    print("BLAH")
    print(get_fibonacci_mod_m(n, m))
