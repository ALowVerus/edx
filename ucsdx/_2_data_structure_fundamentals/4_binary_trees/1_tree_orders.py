# python3

import sys, threading

sys.setrecursionlimit(10 ** 6)  # max depth of recursion
threading.stack_size(2 ** 27)  # new thread will get stack of such size


class TreeOrders:
    def read(self):
        self.n = int(sys.stdin.readline())
        self.key = [0 for i in range(self.n)]
        self.left = [0 for i in range(self.n)]
        self.right = [0 for i in range(self.n)]
        for i in range(self.n):
            [a, b, c] = map(int, sys.stdin.readline().split())
            self.key[i] = a
            self.left[i] = b
            self.right[i] = c
        back_pointers = {}
        for i in range(self.n):
            back_pointers[self.left[i]] = i
            back_pointers[self.right[i]] = i
        key = -1
        while key in back_pointers:
            key = back_pointers[key]
        self.root = key

    def inOrder(self):
        result = []

        # Finish the implementation
        # You may need to add a new recursive method to do that
        def recurse(i, t):
            if t.left[i] != -1:
                recurse(t.left[i], t)
            result.append(self.key[i])
            if t.right[i] != -1:
                recurse(t.right[i], t)

        recurse(self.root, self)
        return result

    def preOrder(self):
        result = []

        # Finish the implementation
        # You may need to add a new recursive method to do that
        def recurse(i, t):
            result.append(self.key[i])
            if t.left[i] != -1:
                recurse(t.left[i], t)
            if t.right[i] != -1:
                recurse(t.right[i], t)

        recurse(self.root, self)
        return result

    def postOrder(self):
        result = []

        # Finish the implementation
        # You may need to add a new recursive method to do that
        def recurse(i, t):
            if t.left[i] != -1:
                recurse(t.left[i], t)
            if t.right[i] != -1:
                recurse(t.right[i], t)
            result.append(self.key[i])

        recurse(self.root, self)
        return result


def main():
    tree = TreeOrders()
    tree.read()
    print(" ".join(str(x) for x in tree.inOrder()))
    print(" ".join(str(x) for x in tree.preOrder()))
    print(" ".join(str(x) for x in tree.postOrder()))


threading.Thread(target=main).start()
