# Uses python3
import sys


def bipartite(adj):
    colors = [None for _ in adj]
    for i in range(len(adj)):
        if colors[i] is None:
            colors[i] = True
            q = [[i, 0]]
            while q:
                if q[-1][1] < len(adj[q[-1][0]]):
                    q[-1][1] += 1
                    if colors[adj[q[-1][0]][q[-1][1] - 1]] is colors[q[-1][0]]:
                        return 0
                    elif colors[adj[q[-1][0]][q[-1][1] - 1]] is None:
                        colors[adj[q[-1][0]][q[-1][1] - 1]] = not colors[q[-1][0]]
                        q.append([adj[q[-1][0]][q[-1][1] - 1], 0])
                else:
                    q.pop()
    return 1


if __name__ == '__main__':
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n, m = data[0:2]
    data = data[2:]
    edges = list(zip(data[0:(2 * m):2], data[1:(2 * m):2]))
    adj = [[] for _ in range(n)]
    for (a, b) in edges:
        adj[a - 1].append(b - 1)
        adj[b - 1].append(a - 1)
    print(bipartite(adj))
