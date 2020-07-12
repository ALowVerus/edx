# python3
import sys


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


def process_text_to_adj(lines):
    pairs = [tuple(line.split('|')) for line in lines]
    # print(pairs)
    adjacency_list = {}
    for a, b in pairs:
        if (a[:-1], b[:-1]) not in adjacency_list:
            adjacency_list[(a[:-1], b[:-1])] = {}
        if (a[1:], b[1:]) not in adjacency_list[(a[:-1], b[:-1])]:
            adjacency_list[(a[:-1], b[:-1])][(a[1:], b[1:])] = 0
        adjacency_list[(a[:-1], b[:-1])][(a[1:], b[1:])] += 1
    # print(adjacency_list)
    return adjacency_list


def generate_string_from_kmer_path(k, d, kmers):
    a = ''.join([s[0][0] for s in kmers[:-1]]) + kmers[-1][0]
    b = ''.join([s[1][0] for s in kmers[:-1]]) + kmers[-1][1]
    print(a, b)
    return a[:k+d] + b


if __name__ == "__main__":
    # k, d = map(int, sys.stdin.readline().strip().split())
    # paired_comp = [line.strip() for line in sys.stdin if line.strip()]
    # k, d = 4, 2
    # paired_comp = ["ACAC|CTCT", "ACAT|CTCA", "CACA|TCTC", "GACA|TCTC"]
    k, d = 2, 1
    paired_comp = ["GG|GA", "GT|AT", "TG|TA", "GA|AC", "AT|CT"]
    adj = process_text_to_adj(paired_comp)
    for k, v in adj.items():
        print(k, v)
    path = reconstruct(adj)
    print(path)
    res = generate_string_from_kmer_path(k, d, path)
    print(res)

