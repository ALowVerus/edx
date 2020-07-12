# Uses python3
import sys


def acyclic(adj):
    seen = set()
    for i in range(len(adj)):
        q_set = {i}
        q_list = [[i, 0]]
        while q_list:
            if q_list[-1][1] < len(adj[q_list[-1][0]]):
                q_list[-1][1] += 1
                if adj[q_list[-1][0]][q_list[-1][1]-1] in q_set:
                    return 1
                elif adj[q_list[-1][0]][q_list[-1][1]-1] not in seen:
                    seen.add(adj[q_list[-1][0]][q_list[-1][1]-1])
                    q_set.add(adj[q_list[-1][0]][q_list[-1][1]-1])
                    q_list.append([adj[q_list[-1][0]][q_list[-1][1]-1], 0])
            else:
                q_set.remove(q_list[-1][0])
                q_list.pop()
    return 0


if __name__ == '__main__':
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n, m = data[0:2]
    data = data[2:]
    edges = list(zip(data[0:(2 * m):2], data[1:(2 * m):2]))
    adj = [[] for _ in range(n)]
    for (a, b) in edges:
        adj[a - 1].append(b - 1)
    print(acyclic(adj))
