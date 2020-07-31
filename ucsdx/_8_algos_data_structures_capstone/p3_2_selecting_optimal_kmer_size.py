# python3
import sys


def reconstruct(adj_list, counts_matter=False):
    """Reconstructs a string from its k-mer composition"""
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
            return None
    if len(starts) > 1 or len(ends) > 1:
        return None

    # Generate the cycle
    from copy import deepcopy
    adj_list = deepcopy(adj_list)

    def search_path(key, path, indent=0):
        while len(adj_list[key]) > 0:
            k, v = adj_list[key].popitem()
            if counts_matter and v > 1:
                adj_list[key][k] = v - 1
            search_path(k, path, indent + 1)
        path.append(key)

    path = []
    # print('Starts, ends:', starts, ends)
    search_path(list(adj_list.keys())[0], path)
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


def get_kmers(k, s):
    return [s[i:i+k] for i in range(len(s) - k + 1)]


testing = False
from random import choice, randint, shuffle
if __name__ == "__main__":
    if not testing:
        reads = [line.strip() for line in sys.stdin if line.strip()]
    else:
        randomly_generating = False
        if randomly_generating:
            read_len = 100
            s_len = 1618
            read_offset = 2
            reads_count = 400
            s = ''.join([choice('ACTG') for i in range(s_len)])
            reads = [s[i:(i + read_len)] + s[:(i + read_len) % s_len if i + read_len > s_len else 0]
                     for i in range(0, s_len, read_offset)]
            shuffle(reads)
            read_choices = [randint(0, len(reads) - 1) for i in range(reads_count)]
            reads = [reads[i] for i in read_choices]
        else:
            s = "ATATATATATATATAT"
            s_len = len(s)
            read_len = 6
            read_offset = 2
            reads = [s[i:(i + read_len)] + s[:(i + read_len) % s_len if i + read_len > s_len else 0]
                     for i in range(0, s_len, read_offset)]
            print(reads)
        print('Testing on string:', s)
    running_binary_search = False
    if running_binary_search:
        k_min = 2
        k_max = len(reads[0]) + 1
        hits = 0
        while k_min != k_max - 1 and hits < 100:
            hits += 1
            k_curr = (k_min + k_max) // 2
            if testing:
                print('K bounds:', k_min, k_curr, k_max)
            patterns = []
            for read in reads:
                patterns.extend(get_kmers(k_curr, read))
            adj = process_text_to_adj(patterns)
            if testing:
                print(adj)
            path = reconstruct(adj, counts_matter=False)
            if path is None:
                k_max = k_curr
            else:
                k_min = k_curr
        if hits == 100:
            raise Exception("You've somehow descended into a loop.")
        print(k_min)
    else:
        best_k = 1
        for k in range(2, len(reads[0]) + 1):
            patterns = []
            for read in reads:
                patterns.extend(get_kmers(k, read))
            adj = process_text_to_adj(patterns)
            if testing:
                print(adj)
            path = reconstruct(adj, counts_matter=False)
            if path is not None:
                best_k = k
        print(best_k)

