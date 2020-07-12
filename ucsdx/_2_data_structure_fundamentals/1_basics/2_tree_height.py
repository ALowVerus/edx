# python3
# Get the height of a certain tree.

import sys
import threading


def compute_height(parents):
    tree = {}
    for child_i, parent_i in enumerate(parents):
        if parent_i not in tree:
            tree[parent_i] = []
        tree[parent_i].append(child_i)

    # queue-based solution
    q = [[-1, 0, 0]]
    while q[0][2] == 0:
        if q[-1][0] in tree and q[-1][1] < len(tree[q[-1][0]]):
                next_target = tree[q[-1][0]][q[-1][1]]
                q[-1][1] += 1
                q.append([next_target, 0, 0])
        else:
            q[-2][2] = max([q[-2][2], q[-1][2] + 1])
            q.pop()
    return q[0][2]

    # Tried this, got blasted by segfault
    # def recurse(i):
    #     if i not in tree:
    #         return 0
    #     return max([recurse(child_i) for child_i in tree[i]]) + 1
    # return recurse(-1)


def main():
    n = int(input())
    parents = list(map(int, input().split()))
    print(compute_height(parents))


# In Python, the default limit on recursion depth is rather low,
# so raise it here for this problem. Note that to take advantage
# of bigger stack, we have to launch the computation in a new thread.
sys.setrecursionlimit(10 ** 7)  # max depth of recursion
threading.stack_size(2 ** 27)  # new thread will get stack of such size
threading.Thread(target=main).start()
