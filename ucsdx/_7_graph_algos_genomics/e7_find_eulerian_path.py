# python3
import sys
from re import findall


def find_eulerian_path(adj_list):
    """Finds an Eulerian path in the given graph

    Args:
        graph:      a list of strings containing edges in the graph; one
                    string may correspond to multiple edges if it is of the
                    form "X -> Y,Z"

    Returns:
        a string containing an Eulerian path through the given graph
    """
    # Validate the graph for the possibility of a cycle
    inverse_adj_list = {}
    null_dests = set()
    for source, destinations in adj_list.items():
        if source not in inverse_adj_list:
            inverse_adj_list[source] = set()
        for destination in destinations:
            if destination not in inverse_adj_list:
                inverse_adj_list[destination] = set()
            if destination not in adj_list:
                null_dests.add(destination)
            inverse_adj_list[destination].add(source)
    for destination in null_dests:
        adj_list[destination] = set()
    # Generate start and end locations
    starts, ends = [], []
    for key in adj_list:
        if len(inverse_adj_list[key]) == len(adj_list[key]):
            pass
        elif len(inverse_adj_list[key]) == len(adj_list[key]) - 1:
            starts.append(key)
        elif len(inverse_adj_list[key]) == len(adj_list[key]) + 1:
            ends.append(key)
        else:
            raise Exception("Your input adjacency list has no Eulerian path.")
    # Generate the cycle
    from copy import deepcopy
    adj_list = deepcopy(adj_list)

    def search_path(key, path, indent=0):
        while len(adj_list[key]) > 0:
            search_path(adj_list[key].pop(), path, indent+1)
        path.append(key)

    path = []
    search_path(starts[0], path)
    path.reverse()
    return path


if __name__ == "__main__":
    lines = sys.stdin.read().strip().splitlines()
#     lines = """
# 0 -> 2
# 1 -> 3
# 2 -> 1
# 3 -> 0,4
# 6 -> 3,7
# 7 -> 8
# 8 -> 9
# 9 -> 6
#     """.split('\n')[1:-1]
    adj = {int(findall(r'^(.*) ->', s)[0]): {int(c) for c in findall(r'-> (.*)', s)[0].split(',')} for s in lines}
    path = find_eulerian_path(adj)
    print('->'.join(map(str, path)))
