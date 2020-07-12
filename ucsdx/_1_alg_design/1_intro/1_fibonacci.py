# Uses python3
def calc_fib(n):
    res = {0: 0, 1: 1}

    def recurse(n):
        if n not in res:
            recurse(n - 1)
            recurse(n - 2)
            res[n] = res[n - 1] + res[n - 2]

    recurse(n)
    return res[n]


n = int(input())
print(calc_fib(n))
