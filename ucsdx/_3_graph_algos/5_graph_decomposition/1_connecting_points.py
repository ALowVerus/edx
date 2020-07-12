#Uses python3
import sys
import math
from heapq import *


# def minimum_distance(x, y):
#     points = {(x[i], y[i]) for i in range(len(x))}
#     root = points.pop()
#     points.add(root)
#     h = [(0., root)]
#     result = 0.
#     while h:
#         cost, neighbor = heappop(h)
#         if neighbor in points:
#             result += cost
#             points.remove(neighbor)
#             for target in points:
#                 heappush(h, (math.sqrt((target[0]-neighbor[0]) ** 2 + (target[1]-neighbor[1]) ** 2), target))
#     return result

class Database:
    def __init__(self):
        self.items = set()
        self.set_count = 0
        self.ranks = {}
        self.parents = {}
        self.children = {}

    def get_root(self, src):
        src_parent = src
        while self.parents[src_parent] != src_parent:
            src_parent = self.parents[src_parent]
        return src_parent

    def insert(self, target):
        self.items.add(target)
        self.ranks[target] = 0
        self.parents[target] = target
        self.children[target] = []
        self.set_count += 1

    def are_connected(self, src, dst):
        return self.get_root(src) == self.get_root(dst)

    def merge(self, src, dst):
        src_parent = self.get_root(src)
        dst_parent = self.get_root(dst)
        # If the source and destination have the same parent, they are in a linked group.
        if src_parent == dst_parent:
            return False
        # If one component outweighs the other, place the smaller under the greater.
        elif self.ranks[src_parent] > self.ranks[dst_parent]:
            self.parents[dst_parent] = src_parent
            self.children[src_parent].append(dst_parent)
        elif self.ranks[dst_parent] > self.ranks[src_parent]:
            self.parents[src_parent] = dst_parent
            self.children[dst_parent].append(src_parent)
        # If the two components are of matching rank, set one beneath the other and increase the new parent's rank.
        else:
            self.parents[src_parent] = dst_parent
            self.children[dst_parent].append(src_parent)
            self.ranks[dst_parent] += 1
        self.set_count -= 1
        return True


def minimum_distance(x, y):
    #write your code here
    points = {(x[i], y[i]) for i in range(len(x))}
    edges = sorted([tuple(sorted([p0, p1])) for p0 in points for p1 in points if p0 != p1],
                   key=lambda e: (e[0][0]-e[1][0]) ** 2 + (e[0][1]-e[1][1]) ** 2)
    groups = Database()
    result = 0.
    for p0, p1 in edges:
        if p0 not in groups.items:
            groups.insert(p0)
        if p1 not in groups.items:
            groups.insert(p1)
        if not groups.are_connected(p0, p1):
            result += math.sqrt((p0[0]-p1[0]) ** 2 + (p0[1]-p1[1]) ** 2)
            groups.merge(p0, p1)
    return result



if __name__ == '__main__':
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n = data[0]
    x = data[1::2]
    y = data[2::2]
    print("{0:.9f}".format(minimum_distance(x, y)))
