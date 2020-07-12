# python3
import sys
import threading

from ucsdx._5_string_processing.data_structures.suffix_tree import SuffixTreeLinear

sys.setrecursionlimit(10 ** 7)  # max depth of recursion
threading.stack_size(2 ** 30)  # new thread will get stack of such size


def find_occurrences(s, a):
    # Generate a source tree
    if s[-1] != '$':
        s = s + '$'
    else:
        s = s + '%'
    source_tree = SuffixTreeLinear(s)
    # For each pattern, follow down the tree to find the root of all its matches
    top_nodes = []
    for t in a:
        # print(t)
        node = source_tree.root
        i = 0
        works = True
        while works and i < len(t):
            # print(i, str(node))
            if t[i] in node.children:
                # print('t[i]', t[i])
                child = node.children[t[i]]
                edge_length = min([len(t)-i, child.edge_length])
                if str(child)[:edge_length] == t[i:i + edge_length]:
                    node = child
                    i += child.edge_length
                else:
                    works = False
            else:
                works = False
        if works:
            top_nodes.append([node, i])
    # Search through the descendants of all identified top nodes, use hashing to avoid retreading
    hits = set()
    seen_node_ids = set()
    stack = []
    for node, depth in top_nodes:
        if id(node) not in seen_node_ids:
            seen_node_ids.add(id(node))
            stack.append([node, depth])
    while stack:
        node, depth = stack.pop()
        if len(node.children) == 0:
            hits.add(node.i1 - depth)
        else:
            for k, child in node.children.items():
                if id(child) not in seen_node_ids:
                    seen_node_ids.add(id(child))
                    stack.append([child, depth + child.edge_length])
    return hits


if __name__ == '__main__':
    text = sys.stdin.readline().strip()
    pattern_count = int(sys.stdin.readline().strip())
    patterns = sys.stdin.readline().strip().split()
    # text = 'AAA'
    # patterns = ['A']
    # text = 'ATATATA'
    # patterns = ['ATA', 'C', 'TATAT']
    occs = find_occurrences(text, patterns)
    print(" ".join(map(str, occs)))


