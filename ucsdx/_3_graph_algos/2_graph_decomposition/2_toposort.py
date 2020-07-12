# Uses python3
import sys


def toposort(adj):
    # write your code here
    ordering = []
    seen = set()
    for i in range(len(adj)):
        if i not in seen:
            seen.add(i)
            q_list = [[i, 0]]
            while q_list:
                if q_list[-1][1] < len(adj[q_list[-1][0]]):
                    q_list[-1][1] += 1
                    if adj[q_list[-1][0]][q_list[-1][1] - 1] not in seen:
                        seen.add(adj[q_list[-1][0]][q_list[-1][1] - 1])
                        q_list.append([adj[q_list[-1][0]][q_list[-1][1] - 1], 0])
                else:
                    ordering.append(q_list.pop()[0])
    return ordering[::-1]
    # adj_inv = [[] for i in adj]
    # for i, targets in enumerate(adj):
    #     for t in targets:
    #         adj_inv[t].append(i)
    # seen = set()
    # while ordering:
    #     i = ordering.pop()


if __name__ == '__main__':
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n, m = data[0:2]
    data = data[2:]
    edges = list(zip(data[0:(2 * m):2], data[1:(2 * m):2]))
    adj = [[] for _ in range(n)]
    for (a, b) in edges:
        adj[a - 1].append(b - 1)
    order = toposort(adj)
    for x in order:
        print(x + 1, end=' ')
