# python3


import sys
import threading

sys.setrecursionlimit(10 ** 7)  # max depth of recursion
threading.stack_size(2 ** 30)  # new thread will get stack of such size


from ucsdx._5_string_processing.data_structures.suffix_tree import SuffixTreeLinear


case = 5
if case == 0:
    p = "AAA"
    q = "TTT"
elif case == 1:
    p = "CCAAGCTGCTAGAGG"
    q = "CATGCTGGGCTGGCT"
elif case == 2:
    p = 'ATGCGATGACCTGACTGA'
    q = 'CTCAACGTATTGGCCAGA'
elif case == 3:
    p = "AG"
    q = "CT"
else:
    p = sys.stdin.readline().strip()
    q = sys.stdin.readline().strip()

if p == q:
    ans = p
else:
    # Generate the tree
    s = "{}#{}$".format(p, q)
    tree = SuffixTreeLinear(s)
    # DFS to find the shortest path
    container = {'best_length': len(p), 'ans': (0, len(p))}
    def dfs_identify_best(node, depth=0, indent=0):
        hits_p = s[node.i1-1] == '$' and node.edge_length >= len(q) + 3
        hits_q = s[node.i1-1] == '$' and node.edge_length < len(q) + 1
        # print('   ' * indent, 'Hitting node {} with substring {}'.format(node.index, str(node)))
        for k, v in node.children.items():
            # print('   ' * indent, 'depth', depth)
            # print('   ' * indent, 'Recursing into node {} through {}'.format(node.index, k))
            child_hits_p, child_hits_q = dfs_identify_best(v, depth + (v.edge_length if v.i1 != len(s) else 1), indent + 1)
            hits_p |= child_hits_p
            hits_q |= child_hits_q
        # print('   ' * indent, 'Final depth: {}'.format(depth))
        if hits_p and not hits_q:
            # print('   ' * indent, 'Node {} hits p but not q. Prospective addition {}, length {}. Existing len is {}.'.format(
            #     node.index, s[node.i0 - depth + 1:node.i0 + 1], depth, container['best_length']))
            if depth <= container['best_length']:
                container['best_length'] = depth
                container['ans'] = (node.i0 - depth + 1, node.i0 + 1)
                # print('   ' * indent, 'Setting answer to {}, so string is {}.'.format(container['ans'], s[container['ans'][0]:container['ans'][1]]))
        return hits_p, hits_q
    dfs_identify_best(tree.root)
    ans = s[container['ans'][0]:container['ans'][1]]

sys.stdout.write(ans + '\n')
