#Uses python3
import sys


def shortest_paths(adj, cost, s, distance, reachable, shortest):
    # Combine adj and cost
    a = {}
    for i in range(len(adj)):
        a[i] = {}
        for j, c in zip(adj[i], cost[i]):
            a[i][j] = c
    # DFS from s to get subgraph
    b = {s: {}}
    seen = {s}
    q = {s}
    while q:
        i = q.pop()
        for j, c in a[i].items():
            if j not in seen:
                seen.add(j)
                q.add(j)
                b[j] = {}
            b[i][j] = c
    for i in range(len(reachable)):
        reachable[i] = int(i in b)
    # Run Bellman-Ford on the resulting subgraph
    distance[s] = 0
    old_dists = {i: distance[i] for i in a}
    for k in range(len(a)+1):
        new_dists = {i: old_dists[i] for i in old_dists}
        for i in old_dists:
            for j, c in a[i].items():
                if old_dists[i] + a[i][j] < old_dists[j]:
                    new_dists[j] = old_dists[i] + a[i][j]
        old_dists = new_dists
    for k in range(len(a)+1):
        new_dists = {i: old_dists[i] for i in old_dists}
        for i in old_dists:
            for j, c in a[i].items():
                if old_dists[i] + a[i][j] < old_dists[j]:
                    new_dists[j] = old_dists[i] + a[i][j]
                    shortest[j] = 0
        old_dists = new_dists
    for i in range(len(distance)):
        distance[i] = old_dists[i]


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
    s = data[0]
    s -= 1
    distance = [10**19] * n
    reachable = [0] * n
    shortest = [1] * n
    shortest_paths(adj, cost, s, distance, reachable, shortest)
    for x in range(n):
        if reachable[x] == 0:
            print('*')
        elif shortest[x] == 0:
            print('-')
        else:
            print(distance[x])

