#python3
import sys


def overlap_graph(reads):
    """Creates an overlap graph from a list of k-mers

    Args:
        patterns:       a list of string k-mers

    Returns:
        a string containing an adjacency list representation of the overlap
        graph as described in the problem specification
    """
    to_dict = {}
    for read in reads:
        if read[:-1] not in to_dict:
            to_dict[read[:-1]] = set()
        to_dict[read[:-1]].add(read)
    connections = {}
    for read in reads:
        if read[1:] in to_dict:
            connections[read] = to_dict[read[1:]]
    return connections


if __name__ == "__main__":
    patterns = sys.stdin.read().strip().splitlines()
    # patterns = "AAG,AGA,ATT,CTA,CTC,GAT,TAC,TCT,TCT,TTC".split(',')
    adj = overlap_graph(patterns)
    for s, t in adj.items():
        print('{}->{}'.format(s, ','.join(t)))
