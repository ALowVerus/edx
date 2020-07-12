# Uses python3

import sys


def actual_negative_cycle(a):
    count = 0
    hit_something = True
    last_costs = [0 for _ in adj]
    while count < len(adj) and hit_something:
        new_costs = [n for n in last_costs]
        hit_something = False
        for i in range(len(a)):
            for j, c in a[i].items():
                if last_costs[i] + a[i][j] < new_costs[j]:
                    new_costs[j] = last_costs[i] + a[i][j]
                    hit_something = True
        last_costs = new_costs
        count += 1
    return hit_something


# txt = """
# 4 4
# 1 2 -5
# 4 1 2
# 2 3 2
# 3 1 1
# """
#
# lines = [list(map(int, line.split(' '))) for line in txt.split("\n")[1:-1]]
# n, m = lines[0]
# adj = [{} for _ in range(n)]
# for a, b, c in lines[1:]:
#     adj[a-1][b-1] = c
# print(actual_negative_cycle(adj))
# exit()


def negative_cycle(adj, cost):
    a = {}
    for i in range(len(adj)):
        a[i] = {}
        for j, c in zip(adj[i], cost[i]):
            a[i][j] = c
    return int(actual_negative_cycle(a))


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
    print(negative_cycle(adj, cost))
