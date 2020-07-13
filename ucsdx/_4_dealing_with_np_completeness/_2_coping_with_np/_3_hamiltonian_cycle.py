# python3

def read_data():
    # n, m = 4, 6
    n, m = map(int, input().split())
    graph = {}
    for i in range(1, n+1):
        graph[i] = {}
    for _ in range(m):
        u, v, weight = map(int, input().split())
        graph[u][v] = graph[v][u] = weight
    # txt = """
    # 1 2 20
    # 1 3 42
    # 1 4 35
    # 2 3 30
    # 2 4 34
    # 3 4 12
    # """
    # lines = txt.split('\n')[1:-1]
    # for line in lines:
    #     u, v, weight = map(int, line.split())
    #     graph[u][v] = graph[v][u] = weight
    return graph


def print_answer(path_weight, path):
    print(path_weight)
    if path_weight == -1:
        return
    print(' '.join(map(str, path)))


# Find a path through the converted graph
def bellman_held_karp(graph, get_max=False):
    n = len(graph)
    # Instantiate an array to hold referral information
    array = [[None for i in range(n)] for j in range(2 ** n)]
    # For every item, set the subset of size 1 that contains it.
    # We can do this i, 2**i notation because the subsets are arranged like so:
    # a, b, ab, c, ac, bc, abc, d, ...
    # which means that all the information required to check the next item is already given, in all cases
    for i in range(n):
        array[2 ** i][i] = (0, None)
    # While iterating over all subsets
    for i in range(2 ** n):
        # And all the possible endpoints for those subsets
        for j in range(n):
            # If the j-th bit in i in set; i.e. if we have started to consider the item at hand.
            # We do this because of the way we have set up the bit-masking such that each bit matches a new item.
            # i.e. the first subset in 2 ** i is a, the second is b, the fourth c, the 8th d.
            # To account for this, we must start our indexing at 1, so 1 is a.
            # If 0 is a, these shenanigans fail.
            if i & (2 ** j):
                # We know that j is up for consideration, so we can now check its precursors.
                for k in range(n):
                    # If A) the subset at hand contains the precursor
                    # and B) the precursor is linked to j,
                    if i & (2 ** k) and k in graph[j]:
                        # If the subset that leads to j can be visited,
                        if array[i ^ (2 ** j)][k] is not None:
                            # We can visit this subset.
                            # If the current cell value is None or less that the generated value, overwrite.
                            if array[i][j] is None or \
                                    (not get_max and array[i][j][0] > array[i ^ (2 ** j)][k][0] + graph[j][k]) or \
                                    (get_max and array[i][j][0] < array[i ^ (2 ** j)][k][0] + graph[j][k]):
                                array[i][j] = (array[i ^ (2 ** j)][k][0] + graph[j][k], k)
    # If any of the items in the final set, which represents the full set, are True, we found a good end.
    for j in range(n):
        if array[(2 ** n) - 1][j]:
            best_ans = array[(2 ** n) - 1][j][0]
            best_path = [j]
            x = (2 ** n) - 1
            while len(best_path) < n:
                best_path.append(array[x][best_path[-1]][1])
                x = x ^ (2 ** (best_path[-2]))
            res = (best_ans, best_path)
            return res
    return None


# The deterministic Bellman-Held-Karp algo, with its n^2 * 2^n complexity, never fails.
def get_hamiltonian_cycle(graph, get_max=False):
    # Convert graph keys to integers
    keys_to_integers = {}
    n = 0
    converted_graph = {}
    for s, sub in graph.items():
        if s not in keys_to_integers:
            keys_to_integers[s] = n
            n += 1
        si = keys_to_integers[s]
        if si not in converted_graph:
            converted_graph[si] = {}
        for f, v in sub.items():
            if f not in keys_to_integers:
                keys_to_integers[f] = n
                n += 1
            sf = keys_to_integers[f]
            converted_graph[si][sf] = v
    # Add a start node, an end node, and a copy of the final node
    converted_graph[n + 0] = {}  # Copy of final node
    converted_graph[n + 1] = {}  # Start node
    converted_graph[n + 2] = {}  # End node
    # Copy the connections of the last node into the duplicate
    for t in converted_graph[n - 1]:
        converted_graph[n + 0][t] = converted_graph[n - 1][t]
        converted_graph[t][n + 0] = converted_graph[t][n - 1]
    # Connect the start node to the original and the end node to the dupe
    converted_graph[n + 1][n + 0] = 0
    converted_graph[n + 0][n + 1] = 0
    converted_graph[n - 1][n + 2] = 0
    converted_graph[n + 2][n - 1] = 0

    res = bellman_held_karp(converted_graph, get_max=get_max)

    if res is None:
        return None
    else:
        integers_to_keys = {val: key for key, val in keys_to_integers.items()}
        try:
            res = res[0], [integers_to_keys[i] for i in res[1][2:-1]]
        except KeyError:
            res = res[0], [integers_to_keys[i] for i in res[1][1:-2]]
        return res


def optimal_path(graph):
    res = get_hamiltonian_cycle(graph)
    return (-1, []) if res is None else res


if __name__ == '__main__':
    print_answer(*optimal_path(read_data()))
