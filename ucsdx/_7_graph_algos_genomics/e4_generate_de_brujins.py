#python3
import sys


def de_bruijn(n, s):
    """Creates a de Bruijn graph from a string given a value of k

    Args:
        k:          the length of strings represented by edges in the
                    de Bruijn graph
        text:       the string from which the de Bruijn grpah will be
                    constructed

    Returns:
        a string containing an adjacency list representation of the de Bruijn
        graph as described in the problem specification
    """
    reads = [s[i:i + int(n)] for i in range(len(s) - int(n) + 1)]
    adjacency_list = {}
    for read in reads:
        if read[:-1] not in adjacency_list:
            adjacency_list[read[:-1]] = set()
        adjacency_list[read[:-1]].add(read[1:])
    return adjacency_list


if __name__ == "__main__":
    k = int(sys.stdin.readline().strip())
    text = sys.stdin.readline().strip()
    # k, text = 3, 'ACGTGTATA'
    adj = de_bruijn(k, text)
    print('\n'.join(['{}->{}'.format(s, ','.join(t)) for s, t in adj.items()]))
