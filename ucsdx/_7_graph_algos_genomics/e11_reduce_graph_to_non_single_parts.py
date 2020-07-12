# python3
import sys
from copy import deepcopy


def reduce_to_contigs(adj):
    """Finds all contigs in a de Bruijn graph made from patterns

    Args:
        patterns:       a list of strings containing all k-mers to
                        be used to construct a de Bruijn graph

    Returns:
        a string with all the contigs in the format specified by
        the problem description
    """
    adj = deepcopy(adj)
    # TODO: your code here
    reverse_adj = {}
    # print(adj)
    for s in adj:
        if s not in reverse_adj:
            reverse_adj[s] = {}
        for t in adj[s]:
            if t not in reverse_adj:
                reverse_adj[t] = {}
            if s not in reverse_adj[t]:
                reverse_adj[t][s] = {}
            for p in adj[s][t]:
                c = adj[s][t][p]
                reverse_adj[t][s][p] = c
    # print(reverse_adj)
    nodes = set(adj.keys())
    while nodes:
        s = nodes.pop()
        # print(s, adj)
        out_degree = sum([sum([adj[s][t][p] for p in adj[s][t]]) for t in adj[s]])
        in_degree = sum([sum([reverse_adj[s][t][p] for p in reverse_adj[s][t]]) for t in reverse_adj[s]])
        if in_degree == 1 and out_degree == 1:
            # Secure the required data
            no, ni = list(adj[s].keys())[0], list(reverse_adj[s].keys())[0]
            po, pi = list(adj[s][no].keys())[0], list(reverse_adj[s][ni].keys())[0]
            p = pi[:-len(s)] + po
            if no != s != ni:
                # Rewire the adjacency links
                adj.pop(s)
                adj[ni].pop(s)
                if no not in adj[ni]:
                    adj[ni][no] = {}
                if p not in adj[ni][no]:
                    adj[ni][no][p] = 0
                adj[ni][no][p] += 1
                reverse_adj.pop(s)
                reverse_adj[no].pop(s)
                if ni not in reverse_adj[no]:
                    reverse_adj[no][ni] = {}
                if p not in reverse_adj[no][ni]:
                    reverse_adj[no][ni][p] = 0
                reverse_adj[no][ni][p] += 1
    return adj


def generate_adjacency_list(reads):
    adj = {}
    for read in reads:
        if read[:-1] not in adj:
            adj[read[:-1]] = {}
        if read[1:] not in adj:
            adj[read[1:]] = {}
        if read[1:] not in adj[read[:-1]]:
            adj[read[:-1]][read[1:]] = {}
        if read not in adj[read[:-1]][read[1:]]:
            adj[read[:-1]][read[1:]][read] = 0
        adj[read[:-1]][read[1:]][read] += 1
    return adj


if __name__ == "__main__":
    patterns = [line.strip() for line in sys.stdin if line.strip()]
    # patterns = ["ATG", "ATG", "TGT", "TGG", "CAT", "GGA", "GAT", "AGA"]
    # patterns = ['GAGA', 'AGAG', 'AACG', 'ACGT', 'ACGG']
    adj = generate_adjacency_list(patterns)
    # print(adj)
    reduced_adj = reduce_to_contigs(adj)
    contigs = []
    for s in reduced_adj:
        for t in reduced_adj[s]:
            for p in reduced_adj[s][t]:
                for i in range(reduced_adj[s][t][p]):
                    contigs.append(p)
    print(' '.join(contigs))
