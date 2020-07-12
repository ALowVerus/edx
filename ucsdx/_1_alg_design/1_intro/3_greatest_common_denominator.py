# Uses python3
import sys


def gcd(a, b):
    a, b = sorted([a, b])
    while b % a != 0:
        b, a = a, b % a
    return a


print(gcd(1000000, 1000000))
22

# if __name__ == "__main__":
#     input = sys.stdin.read()
#     a, b = map(int, input.split())
#     print(gcd(a, b))
