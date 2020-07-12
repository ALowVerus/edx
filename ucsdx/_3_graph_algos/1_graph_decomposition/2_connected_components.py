# Uses python3

import sys


def number_of_components(adj):
    component_count = 0
    seen = set()
    for i in range(len(adj)):
        if i not in seen:
            q = {i}
            seen |= q
            while q:
                new = {item for item in set(adj[q.pop()]) if item not in seen}
                seen |= new
                q |= new
            component_count += 1
    return component_count


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
    print(number_of_components(adj))
