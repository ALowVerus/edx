# python3
from ucsdx._5_string_processing.data_structures.suffix_tree import SuffixTreeLinear


def find_occurrences_naive(s, t):
    hits = []
    for genome_i in range(len(s) - len(pattern) + 1):
        pattern_i = 0
        while pattern_i < len(t) and s[genome_i+pattern_i] == t[pattern_i]:
            pattern_i += 1
        if pattern_i == len(t):
            hits.append(genome_i)
    return hits


def find_occurrences_using_tree(s, t):
    # from ucsdx._5_string_processing.data_structures.suffix_tree import SuffixTreeLinear
    tree = SuffixTreeLinear(s + '$')
    curr = tree.root
    i = 0
    while i < len(t) and t[i] in curr.children:
        c = t[i]
        child = curr.children[c]
        i += child.edge_length
        curr = child
    if i < len(t):
        return []
    hits = []
    def recurse(node, depth):
        if len(node.children) == 0:
            # print('Hit!', node.i0, node.i1, node.i1 - depth, s[node.i1 - depth:])
            hits.append(node.i1 - depth)
        else:
            # keys = sorted(list(node.children.keys()))
            for k, child in node.children.items():
                recurse(child, depth + child.edge_length)
    recurse(curr, i)
    return hits


def find_occurrences_kmp(s, t):
    a = [0 for i in range(len(t))]
    for j in range(1, len(t)):
        i = a[j - 1]
        while i > 0 and t[i] != t[j]:
            i = a[i - 1]
        if t[i] == t[j]:
            i += 1
        a[j] = i

    hits = []
    ti = 0
    for si in range(len(s)):
        # print(ti, si, hits)
        while ti > 0 and t[ti] != s[si]:
            ti = a[ti-1]
        if t[ti] == s[si]:
            ti += 1
            if ti == len(t):
                hits.append(si - len(t) + 1)
                ti = a[ti-1]
    # print(hits)
    # print([si for si in range(len(s)) if s[si:si+len(t)] == t])
    return hits


n = 0
if n == 0:
    pattern = input()
    genome = input()
elif n == 1:
    pattern = 'a'
    genome = 'a'
elif n == 2:
    genome = 'abcabacdanmnbaba'
    pattern = 'ab'
elif n == 3:
    genome = 'GATATATGCATATACTT'
    pattern = 'ATAT'
elif n == 4:
    genome = 'adsgwadsxdsgwadsgz'
    pattern = 'dsgwadsgz'
elif n == 5:
    genome = 'AAAATAAATAAAAAAT'
    pattern = 'AAAA'
elif n == 6:
    genome = 'ATATA'
    pattern = 'ATA'
elif n == 7:
    genome = ''
    pattern = ''
else:
    raise Exception()
print(' '.join(map(str, sorted(find_occurrences_kmp(genome, pattern)))))
