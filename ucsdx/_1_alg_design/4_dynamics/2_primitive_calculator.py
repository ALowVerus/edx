# Uses python3
import sys


def optimal_sequence_solution(n):
    backtrackers = {1: 1}

    def recurse(k):
        if k in backtrackers:
            return
        recurse(k - 1)
        if k % 3 == 0:
            recurse(k // 3)
        if k % 2 == 0:
            recurse(k // 2)
        backtrackers[k] = min([k // 3 if k % 3 == 0 else k-1, k // 2 if k % 2 == 0 else k-1, k-1]) + 1

    recurse(n)
    return backtrackers[n]


for i in [1, 5, 96234]:
    print(i, optimal_sequence_solution(i))

# def optimal_sequence(n):
#     sequence = []
#     while n >= 1:
#         sequence.append(n)
#         if n % 3 == 0:
#             n = n // 3
#         elif n % 2 == 0:
#             n = n // 2
#         else:
#             n = n - 1
#     return reversed(sequence)
#
# input = sys.stdin.read()
# n = int(input)
# sequence = list(optimal_sequence(n))
# print(len(sequence) - 1)
# for x in sequence:
#     print(x, end=' ')
