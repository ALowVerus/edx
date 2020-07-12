def gcd(a, b):
    a, b = sorted([a, b])
    while b % a != 0:
        b, a = a, b % a
    return a


def lcm(a, b):
    c = gcd(a, b)
    a //= c
    b //= c
    return a * b * c


import sys
if __name__ == '__main__':
    input = sys.stdin.read()
    a, b = map(int, input.split())
    print(lcm(a, b))

