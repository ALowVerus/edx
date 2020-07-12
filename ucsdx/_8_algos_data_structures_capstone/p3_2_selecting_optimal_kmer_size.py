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
    if len(starts) > 1 or len(ends) > 1:
        return None

    # Generate the cycle
    from copy import deepcopy
    adj_list = deepcopy(adj_list)

    def search_path(key, path, indent=0):
        while len(adj_list[key]) > 0:
            k, v = adj_list[key].popitem()
            if v > 1:
                adj_list[key][k] = v - 1
            search_path(k, path, indent + 1)
        path.append(key)

    path = []
    # print('Starts, ends:', starts, ends)
    if len(starts) == 0:
        search_path(list(adj_list.keys())[0], path)
    else:
        search_path(starts[0], path)
    path.reverse()
    return path


def process_text_to_adj(reads):
    adjacency_list = {}
    for read in reads:
        if read[:-1] not in adjacency_list:
            adjacency_list[read[:-1]] = {}
        if read[1:] not in adjacency_list[read[:-1]]:
            adjacency_list[read[:-1]][read[1:]] = 0
        adjacency_list[read[:-1]][read[1:]] += 1
    return adjacency_list


if __name__ == "__main__":
    reads = [line.strip() for line in sys.stdin if line.strip()]
    k_min = 2
    k_max = len(reads[0]) + 1
    while k_min != k_max - 1:
        k_curr = (k_min + k_max) // 2
        patterns = []
        for read in reads:
            k_mers = [read[i:i+k_curr] for i in range(len(read) - k_curr + 1)]
            patterns.extend(k_mers)
        adj = process_text_to_adj(patterns)
        path = reconstruct(adj)
        if path is None:
            k_max = k_curr
        else:
            k_min = k_curr
    print(k_min)

