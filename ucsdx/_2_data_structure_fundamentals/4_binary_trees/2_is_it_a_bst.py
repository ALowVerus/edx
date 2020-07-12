#!/usr/bin/python3

import sys, threading

sys.setrecursionlimit(10 ** 7)  # max depth of recursion
threading.stack_size(2 ** 25)  # new thread will get stack of such size


def IsBinarySearchTree(tree):
    # Implement correct algorithm here
    if len(tree) < 2:
        return True
    back_pointers = {}
    for i in range(len(tree)):
        back_pointers[tree[i][1]] = i
        back_pointers[tree[i][2]] = i
    root = -1
    while root in back_pointers:
        root = back_pointers[root]
    q = [(root, None, None)]
    while q:
        parent_i, left_bound, right_bound = q.pop()
        left_i = tree[parent_i][1]
        right_i = tree[parent_i][2]
        # Left kiddo
        if left_i == -1:
            pass
        elif tree[parent_i][0] <= tree[left_i][0] or (left_bound is not None and tree[left_i][0] < left_bound):
            return False
        elif tree[parent_i][0] > tree[left_i][0]:
            q.append((tree[parent_i][1], left_bound, tree[parent_i][0] if right_bound is None else max([tree[parent_i][0], right_bound])))
        # Right kiddo
        if right_i == -1:
            pass
        elif tree[parent_i][0] > tree[right_i][0] or (right_bound is not None and tree[right_i][0] > right_bound):
            return False
        elif tree[parent_i][0] <= tree[right_i][0]:
            q.append((tree[parent_i][2], tree[parent_i][0] if left_bound is None else max([tree[parent_i][0], left_bound]), right_bound))
    return True


def main():
    nodes = int(sys.stdin.readline().strip())
    tree = []
    for i in range(nodes):
        tree.append(list(map(int, sys.stdin.readline().strip().split())))
    if IsBinarySearchTree(tree):
        print("CORRECT")
    else:
        print("INCORRECT")


threading.Thread(target=main).start()
