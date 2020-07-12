# python3


# Class that handles a suffix trie
class Tree:
    def __init__(self):
        self.counter = 0
        self.root = Tree.Node()

    def load(self, target):
        self.root.load(target, 0)

    def print_tree(self):
        self.root.print_tree(0)

    class Node:
        def __init__(self):
            self.children = {}

        def load(self, s, i):
            if i >= len(s):
                pass
            elif s[i] not in self.children:
                self.children[s[i]] = Tree.Node()
                self.children[s[i]].load(s, i + 1)
            else:
                self.children[s[i]].load(s, i + 1)

        def print_tree(self, parent_i):
            child_i = parent_i + 1
            for c, child in self.children.items():
                print("{}->{}:{}".format(parent_i, child_i, c))
                child_i = child.print_tree(child_i)
            return child_i


def build_trie(patterns):
    tree = Tree()
    for substring in patterns:
        tree.load(substring)
    return tree


if __name__ == "__main__":
    import sys
    patterns = sys.stdin.read().split()[1:]
    # patterns = ['ATAGA', 'ATC', 'GAT']
    tree = build_trie(patterns)
    tree.print_tree()
