# python3
import sys


def de_bruijn(reads):
    """Creates a de Bruijn graph from a collection of k-mers

    Args:
        patterns:       a list of strings containing the k-mer collecion
                        to be made into a de Bruijn graph

    Returns:
        a string containing an adjacency list representation of the de Bruijn
        graph as described in the problem specification
    """
    # TODO: your code here
    adjacency_list = {}
    for read in reads:
        if read[:-1] not in adjacency_list:
            adjacency_list[read[:-1]] = []
        adjacency_list[read[:-1]].append(read[1:])
    return adjacency_list


if __name__ == "__main__":
    patterns = sys.stdin.read().strip().splitlines()
    # patterns = "GAGG,CAGG,GGGG,GGGA,CAGG,AGGG,GGAG".split(',')
    adj = de_bruijn(patterns)
    print('\n'.join(['{}->{}'.format(s, ','.join(t)) for s, t in adj.items()]))
