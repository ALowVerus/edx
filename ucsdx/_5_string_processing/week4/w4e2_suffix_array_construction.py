# python3
import sys
from math import log2

from ucsdx._5_string_processing.data_structures.suffix_tree import SuffixTreeLinear


def generate_char_to_ordered_number_mapping(t):
    return {i: c for i, c in enumerate(sorted(list({c for c in t})))}


def build_suffix_array_naive(t):
    suffixes = [(i, t[i:] + "$" * (i + 1)) for i in range(len(t))]
    suffixes = sorted(suffixes, key=lambda e: e[1])
    result = [e[0] for e in suffixes]
    # Implement this function yourself
    return result


def build_suffix_array_tree(s):
    has_dollar = s[-1] == '$'
    if not has_dollar:
        s = s + '$'
    # from ucsdx._5_string_processing.data_structures.suffix_tree import SuffixTreeLinear
    tree = SuffixTreeLinear(s)
    curr = tree.root
    hits = []
    def recurse(node, depth):
        if len(node.children) == 0:
            # print('Hit!', node.i0, node.i1, node.i1 - depth, s[node.i1 - depth:])
            hits.append(node.i1 - depth)
        else:
            # keys = sorted(list(node.children.keys()))
            for k, child in sorted(node.children.items(), key=lambda item: item[0]):
                recurse(child, depth + child.edge_length)
    recurse(curr, 0)
    if not has_dollar:
        hits = hits[1:]
    return hits


def build_suffix_array_radix(t):
    # Minimize the charset
    letters_to_numbers = generate_char_to_ordered_number_mapping(t)
    a = [letters_to_numbers[c] for c in t]
    # Generate an initial ordering of the suffixes
    order = [i for i in range(len(a))]
    # Get the number of required doublings
    doubling_count = int(log2(len(a)))
    # From the last character in, run sequential counting sorts
    for doubling_index in range(doubling_count):
        pass
    return []


if __name__ == '__main__':
    test_type = 5
    if test_type == 0:
        text = sys.stdin.readline().strip()
    elif test_type == 1:
        text = 'AAA$'
    elif test_type == 2:
        text = 'GAC$'
    elif test_type == 3:
        text = 'GAGAGAGA$'
    elif test_type == 4:
        text = 'AACGATAGCGGTAGA$'
    elif test_type == 5:
        text = 'adsqweroiuyaadfoiauyerlakkadfoiuqwerlkajhfoaiuweyrqwlkejhaodifuyqwelkjaldvkjahdvoiaueroqiwueyrlaksdjfhasodfiuyqweoriqer'
    else:
        text = 'A$'
    # naive_res = build_suffix_array_naive(text)
    # print(naive_res)
    tree_res = build_suffix_array_tree(text)
    # print(tree_res)
    # exit()
    # radix_res = build_suffix_array_radix(text)
    p = lambda a: print(" ".join(map(str, a)))
    # p(naive_res)
    p(tree_res)
    # p(radix_res)
