# Uses python3
def calc_fib(n):
    res = {0: 0, 1: 1}
    for i in range(2, n+1):
        res[i] = (res[i - 1] + res[i - 2]) % 10
    return res[n]


n = int(input())
print(calc_fib(n))
