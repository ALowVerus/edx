#Uses python3
import sys
import math


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


def clustering(x, y, k):
    #write your code here
    dist = lambda e: ((e[0][0]-e[1][0]) ** 2 + (e[0][1]-e[1][1]) ** 2) ** 0.5
    points = {(x[i], y[i]) for i in range(len(x))}
    edges = sorted([tuple(sorted([p0, p1])) for p0 in points for p1 in points if p0 != p1], key=dist)
    groups = Database()
    for point in points:
        groups.insert(point)
    ei = 0
    done = False
    while ei < len(edges) and not done:
        p0, p1 = edges[ei]
        if not groups.are_connected(p0, p1):
            if groups.set_count == k:
                done = True
            else:
                groups.merge(p0, p1)
        ei += 1
    return dist(edges[ei-1])


if __name__ == '__main__':
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n = data[0]
    data = data[1:]
    x = data[0:2 * n:2]
    y = data[1:2 * n:2]
    data = data[2 * n:]
    k = data[0]
    print("{0:.9f}".format(clustering(x, y, k)))
