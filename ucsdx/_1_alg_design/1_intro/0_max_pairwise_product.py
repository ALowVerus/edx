# Uses python3
n = int(input())
a = [int(x) for x in input().split()]
assert(len(a) == n)


def max_pairwise_product(a):
    if len(a) < 5:
        result = max([a[i] * a[j] for i in range(0, len(a)-1) for j in range(i+1, len(a))])
    else:
        max_a = max(a)
        a.remove(max_a)
        max_b = max(a)
        a.remove(max_b)
        min_a = min(a)
        a.remove(min_a)
        min_b = min(a)
        a.remove(min_b)
        result = max([min_a * min_b, max_a * max_b])
    return result


print(max_pairwise_product(a))
