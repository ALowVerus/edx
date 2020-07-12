# python3
from re import findall
import sys
import threading

sys.setrecursionlimit(10 ** 7)  # max depth of recursion
threading.stack_size(2 ** 30)  # new thread will get stack of such size


def find_eulerian_cycle(adj_list):
    """Finds an Eulerian cycle in the given graph

    Args:
        graph:      a list of strings containing edges in the graph; one
                    string may correspond to multiple edges if it is of the
                    form "X -> Y,Z"

    Returns:
        a string containing an Eulerian cycle through the given graph
    """
    # Validate the graph for the possibility of a cycle
    inverse_adj_list = {}
    for source, t_dict in adj_list.items():
        for target, count in t_dict.items():
            if target not in inverse_adj_list:
                inverse_adj_list[target] = {}
            inverse_adj_list[target][source] = adj[source][target]
    for key in adj_list:
        if sum([v for k, v in inverse_adj_list[key].items()]) != \
                sum([v for k, v in adj[key].items()]):
            return []
    # Generate the cycle
    from copy import deepcopy
    adj_list = deepcopy(adj_list)

    def search_path(key, path, indent=0):
        while len(adj_list[key]) > 0:
            target, count = adj_list[key].popitem()
            if count > 1:
                adj_list[key][target] = count - 1
            search_path(target, path, indent+1)
        path.append(key)

    path = []
    search_path(list(adj_list.keys())[0], path)
    path.reverse()
    return path


if __name__ == "__main__":
    formatting_style = 1
    if formatting_style == 0:
        lines = sys.stdin.read().strip().splitlines()
        adj = {int(findall(r'^(.*) ->', s)[0]): {int(c) for c in findall(r'-> (.*)', s)[0].split(',')} for s in lines}
        adj = {source: {target: 1 for target in adj[source]} for source in adj}
    elif formatting_style == 1:
        node_count, line_count = map(int, input().split(' '))
        lines = [input() for i in range(line_count)]
        # lines = ['1 2', '2 1']
        # print("LINES")
        # for line in lines:
        #     print(line)
        # print('LINES')
        adj = {}
        for line in lines:
            s, t = line.split(' ')
            if s not in adj:
                adj[s] = {}
            if t not in adj[s]:
                adj[s][t] = 0
            adj[s][t] += 1
    else:
        raise Exception()
    path = find_eulerian_cycle(adj)
    if formatting_style == 0:
        print('->'.join(map(str, path)))
    elif formatting_style == 1:
        print(0 if len(path) == 0 else '1\n' + ' '.join(map(str, path[:-1])))
