# python3
import sys


class Node:
    def __init__(self):
        self.children = {}

    def load(self, s, i):
        if i >= len(s):
            pass
        else:
            if s[i] not in self.children:
                self.children[s[i]] = Node()
            self.children[s[i]].load(s, i + 1)


target = sys.stdin.readline().strip()
n = int(sys.stdin.readline().strip())
patterns = []
for i in range(n):
    patterns.append(sys.stdin.readline().strip())
# target = 'AATCGGGTTCAATCGGGGT'
# patterns = ['ATCG', 'GGGT']


root = Node()
for substring in patterns:
    root.load(substring + '$', 0)
wins = []
for i in range(len(target)):
    curr_node = root
    k = i
    while '$' not in curr_node.children and k < len(target) and target[k] in curr_node.children:
        curr_node = curr_node.children[target[k]]
        k += 1
    if '$' in curr_node.children:
        wins.append(i)
print(' '.join([str(i) for i in wins]))
