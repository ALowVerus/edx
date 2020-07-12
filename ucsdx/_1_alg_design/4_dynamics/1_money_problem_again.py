# Uses python3
import sys


# def get_change(m):
#     baseline = {
#         1: {1: 1, 3: 0, 4: 0},
#         2: {1: 2, 3: 0, 4: 0},
#         3: {1: 0, 3: 1, 4: 0},
#         4: {1: 0, 3: 0, 4: 1},
#         5: {1: 1, 3: 0, 4: 1},
#         6: {1: 0, 3: 2, 4: 0},
#         7: {1: 0, 3: 1, 4: 1},
#         8: {1: 0, 3: 0, 4: 2},
#         9: {1: 1, 3: 0, 4: 2},
#         10: {1: 0, 3: 2, 4: 1},
#         11: {1: 0, 3: 1, 4: 2},
#         12: {1: 0, 3: 0, 4: 3},
#         13: {1: 1, 3: 0, 4: 3},
#         14: {1: 0, 3: 2, 4: 2},
#         15: {1: 0, 3: 1, 4: 3},
#         16: {1: 0, 3: 0, 4: 4},
#         17: {1: 0, 3: 3, 4: 2},
#         18: {1: 0, 3: 2, 4: 3},
#         19: {1: 0, 3: 1, 4: 4},
#         20: {1: 0, 3: 0, 4: 5},
#         21: {1: 0, 3: 3, 4: 3},
#         22: {1: 0, 3: 2, 4: 4},
#         23: {1: 0, 3: 1, 4: 5},
#         24: {1: 0, 3: 0, 4: 6},
#         25: {1: 0, 3: 3, 4: 4},
#         26: {1: 0, 3: 2, 4: 5},
#         27: {1: 0, 3: 1, 4: 6},
#         28: {1: 0, 3: 0, 4: 7},
#         29: {1: 0, 3: 3, 4: 5},
#         30: {1: 0, 3: 2, 4: 6},
#         31: {1: 0, 3: 1, 4: 7},
#         32: {1: 0, 3: 0, 4: 8},
#         33: {1: 0, 3: 3, 4: 6},
#         34: {1: 0, 3: 2, 4: 7},
#         35: {1: 0, 3: 1, 4: 8},
#     }
#     return sum(v for k, v in baseline[m].items())
#
#
# def get_change_dynamic(m, storage=None):
#     if storage is None:
#         storage = {}
#     storage[1] = storage[3] = storage[4] = 1
#     storage[0] = 0
#
#     def recurse(n, storage):
#         if n in storage:
#             pass
#         else:
#             for d in [1, 3, 4]:
#                 if n > d and n - d not in storage:
#                     recurse(n - d, storage)
#             storage[n] = min([storage[n-d] for d in [1, 3, 4] if n-d >= 0]) + 1
#
#     recurse(m, storage)
#     return storage[m]
#
#
# for i in range(1, 36):
#     a, b = get_change_dynamic(i), get_change(i)
#     print(i, a, b, a == b)


if __name__ == '__main__':
    m = int(sys.stdin.read())
    print((m - 1) // 4 + 1 if m != 2 else 2)
