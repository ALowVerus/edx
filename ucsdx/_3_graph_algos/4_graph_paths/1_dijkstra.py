#Uses python3
import sys
from heapq import *


def distance(adj, cost, s, t):
    #write your code here
    a = {}
    for i in range(len(adj)):
        a[i] = {}
        for j, c in zip(adj[i], cost[i]):
            a[i][j] = c
    seen = {}
    h = []
    heappush(h, (0, s))
    while h and h[0][1] != t:
        c, i = heappop(h)
        if i not in seen:
            seen[i] = c
            for j in a[i]:
                heappush(h, (c + a[i][j], j))
    return -1 if not h else h[0][0]


if __name__ == '__main__':
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n, m = data[0:2]
    data = data[2:]
    edges = list(zip(zip(data[0:(3 * m):3], data[1:(3 * m):3]), data[2:(3 * m):3]))
    data = data[3 * m:]
    adj = [[] for _ in range(n)]
    cost = [[] for _ in range(n)]
    for ((a, b), w) in edges:
        adj[a - 1].append(b - 1)
        cost[a - 1].append(w)
    s, t = data[0] - 1, data[1] - 1
    print(distance(adj, cost, s, t))
