# python3


import sys
import threading

sys.setrecursionlimit(10 ** 7)  # max depth of recursion
threading.stack_size(2 ** 30)  # new thread will get stack of such size

PRINTABLE = """0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~"""


class SuffixTreeSquare:
    def __init__(self, s):
        self.s = s
        # Generate a structure to hold the root of the tree
        root = {}
        # Add each of the substrings to the root tree
        for i in range(len(s)):
            curr = root
            # Can't efficiently describe the failure condition, so just use a flag.
            done = False
            while not done:
                # Iterate over a list of the children of the current node until all are checked or a matching start is found
                kiddo_i = 0
                curr_kiddo_indices = list(curr.keys())
                while kiddo_i < len(curr_kiddo_indices) and s[i] != s[curr_kiddo_indices[kiddo_i][0]]:
                    kiddo_i += 1
                # If a matching start not found, add the
                if kiddo_i == len(curr_kiddo_indices):
                    curr[(i, len(s))] = {}
                    done = True
                # If a matching start is found, either descend down the full match or split at the place of divergence
                else:
                    kiddo = curr_kiddo_indices[kiddo_i]
                    j = 0
                    while kiddo[0] + j < len(s) and kiddo[0] + j < kiddo[1] \
                            and i + j < len(s) and s[kiddo[0] + j] == s[i + j]:
                        j += 1
                    # If a full match is found, add to the starting point, but don't add any new nodes
                    if kiddo[0] + j == kiddo[1]:
                        curr = curr[kiddo]
                        i += j
                    # Else
                    else:
                        kiddo_dict = curr.pop(kiddo)
                        intermediary = {(kiddo[0] + j, kiddo[1]): kiddo_dict}
                        curr[(kiddo[0], kiddo[0] + j)] = intermediary
        self.root = root

    def list_all_paths(self):
        res = []
        q = [self.root]
        while q:
            next_item = q.pop()
            for s, t in next_item.items():
                res.append(s)
                q.append(t)
        return res

    def print_tree(self):
        def recurse(node, indent=0):
            for v, t in node.items():
                print('  ' * indent, self.s[v[0]:v[1]], v)
                recurse(t, indent + 1)

        recurse(self.root)


from ucsdx._5_string_processing.data_structures.suffix_tree import SuffixTreeLinear


def test_string(s):
    used_letters = {c for c in s}
    possible_nulls = {c for c in PRINTABLE if c not in used_letters}
    if len(possible_nulls) == 0:
        raise Exception("You've used every printable character in your input string. Try again.")
    end_char = possible_nulls.pop()

    tree = SuffixTreeLinear(s + end_char)
    linear_strings = tree.get_substrings()
    linear_strings = [s for s in [s.replace(end_char, '') for s in linear_strings] if len(s) > 0]
    print("\n".join(linear_strings))


if __name__ == '__main__':
    import sys
    text = sys.stdin.readline().strip()
    test_string(text)
