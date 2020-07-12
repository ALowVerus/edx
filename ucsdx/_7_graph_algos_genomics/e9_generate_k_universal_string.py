# python3


def reconstruct(adj_list):
    """Reconstructs a string from its k-mer composition

    Args:
        k:          the length of k-mers in the k-mer composition
        patterns:   a list of strings containing the k-mer composition

    Returns:
        A string text with k-mer composition equal to patterns
    """
    # TODO: your code here
    # Copy the adjacency list for later use
    from copy import deepcopy
    adj_list = deepcopy(adj_list)
    # Validate the graph for the possibility of a cycle
    inverse_adj_list = {}
    null_dests = set()
    for source, destinations in adj_list.items():
        if source not in inverse_adj_list:
            inverse_adj_list[source] = {}
        for destination in destinations:
            if destination not in inverse_adj_list:
                inverse_adj_list[destination] = {}
            if destination not in adj_list:
                null_dests.add(destination)
            if source not in inverse_adj_list[destination]:
                inverse_adj_list[destination][source] = 0
            inverse_adj_list[destination][source] += adj_list[source][destination]
    for destination in null_dests:
        adj_list[destination] = {}
    # print('->', adj_list)
    # print('<-', inverse_adj_list)
    # Generate start and end locations
    starts, ends = [], []
    for key in adj_list:
        out_degree = sum([v for k, v in adj_list[key].items()])
        in_degree = sum([v for k, v in inverse_adj_list[key].items()])
        if out_degree == in_degree:
            pass
        elif in_degree == out_degree - 1:
            starts.append(key)
        elif in_degree == out_degree + 1:
            ends.append(key)
        else:
            raise Exception("Your input adjacency list has no Eulerian path.")
    # Non-recursively generate a path
    if len(starts) == 0:
        starts.append(list(adj_list.keys())[0])
    path = []
    stack = [starts[0]]
    while stack:
        if len(adj_list[stack[-1]]) > 0:
            k, v = adj_list[stack[-1]].popitem()
            if v > 1:
                adj_list[stack[-1]][k] = v - 1
            stack.append(k)
        else:
            path.append(stack.pop())
    # print('Starts, ends:', starts, ends)
    path.reverse()
    return path


def process_n_to_adj(n):
    formatter = '{0:0' + str(len(bin(2 ** (n-1)))-2) + '}'
    adj = {}
    for i in range(2 ** n):
        edge = formatter.format(int(bin(i)[2:]))
        if edge[:-1] not in adj:
            adj[edge[:-1]] = {}
        if edge[1:] not in adj[edge[:-1]]:
            adj[edge[:-1]][edge[1:]] = 0
        adj[edge[:-1]][edge[1:]] += 1
    return adj


def generate_string_from_kmer_path(kmers):
    return ''.join([s[0] for s in kmers[:-1]]) + kmers[-1]


if __name__ == "__main__":
    n = input()
    n = int(n)
    adj = process_n_to_adj(n)
    path = reconstruct(adj)
    s = generate_string_from_kmer_path(path)[:-n+1]
    print(s)
    # for i in range(2, 15):
    #     print(i)
    #     adj = process_n_to_adj(i)
    #     path = reconstruct(adj)
    #     s = generate_string_from_kmer_path(path)[:-i+1]
    #     formatter = '{0:0' + str(len(bin(2 ** (i-1))) - 2) + '}'
    #     parts = {formatter.format(int(bin(k)[2:])) for k in range(2 ** i)}
    #     print(s)
    #     m = s + s
    #     for k in range(len(s)):
    #         parts.remove(m[k:k+i])
    #     print(parts)
    #     print()

