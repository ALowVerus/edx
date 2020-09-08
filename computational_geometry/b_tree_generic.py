# class TwoThreeTree:
#     def __init__(self):
#         self.head = None
#
#     def insert(self, v):
#         if self.head is None:
#             self.head = TwoThreeTree(None)
#             self.head.keys = [v]
#             self.head.links = [None, None]
#
#     class TreeNode:
#         def __init__(self, parent):
#             self.keys = []
#             self.links = []
#
#         def insert(self, v):
#             i = 0
#             while i < len(self.keys) and self.keys[i] < v:
#                 i += 1
#             if i < len(self.keys):
#                 self.keys.insert(i, v)


class RedBlackTree:
    def __init__(self, cmp=lambda a, b: 1 if a < b else 0 if a == b else -1):
        self.cmp = cmp
        self.head = None
        self.size = 0

        tree_reference = self

        class RedBlackNode:
            def __init__(self, parent, value, load):
                self.tree = tree_reference
                self.color = 'Red'
                self.parent = parent
                self.value = value
                self.load = load
                self.left = None
                self.right = None
                self.prev = None
                self.next = None

            def insert(self, value, load):
                cmp = self.tree.cmp(value, self.value)
                if cmp == 1:
                    if self.left is not None:
                        return self.left.insert(value, load)
                    else:
                        new_node = RedBlackNode(self, value, load)
                        self.left = new_node
                        self.left.prev = self.prev
                        self.left.prev.next = self.left
                        self.prev = self.left
                        self.left.next = self
                        self.left.resolve_conflicts()
                        return new_node
                else:
                    if self.right is not None:
                        return self.right.insert(value, load)
                    else:
                        new_node = RedBlackNode(self, value, load)
                        self.right = new_node
                        self.right.next = self.next
                        self.right.next.prev = self.right
                        self.next = self.right
                        self.right.prev = self
                        self.right.resolve_conflicts()
                        return new_node

            def resolve_conflicts(self):
                # If grandparents do not exist, you've reached the end.
                if type(self.parent) is RedBlackTree or type(self.parent.parent) is RedBlackTree:
                    return
                # If there is no color violation, return
                elif self.color == "Black" or self.parent.color != "Red":
                    return
                # If the item's uncle is red, recolor stuff and keep moving
                elif self.uncle_color == "Red":
                    self.grandparent.right.color = "Black"
                    self.grandparent.left.color = "Black"
                    self.grandparent.color = "Red"
                    self.grandparent.resolve_conflicts()
                # If the item's uncle is
                elif self.uncle_color == "Black":
                    a, b, c = self, self.parent, self.grandparent
                    # Handle triangle cases.
                    if (self is self.parent.left and self.parent is self.grandparent.right) \
                            or (self is self.parent.right and self.parent is self.grandparent.left):
                        self.parent.rotate(self)
                    # Handle line cases.
                    elif (self is self.parent.left and self.parent is self.grandparent.left) \
                            or (self is self.parent.right and self.parent is self.grandparent.right):
                        self.grandparent.rotate(self.parent)
                        b.color = "Black"
                        c.color = "Red"
                    # Handle exception.
                    else:
                        raise Exception("Apparently, we are neither a line not a triangle!")
                    a.resolve_conflicts()
                    b.resolve_conflicts()
                    c.resolve_conflicts()
                # If none of the above cases apply, we are severely fucked.
                else:
                    raise Exception("Critical failure has occurred during conflict resolution.")

            @property
            def grandparent(self):
                return self.parent.parent

            @property
            def uncle_color(self):
                if self.parent is self.grandparent.left:
                    if not (self.grandparent.right is None) and self.grandparent.right.color == "Red":
                        return "Red"
                    return "Black"
                elif self.parent is self.grandparent.right:
                    if not (self.grandparent.left is None) and self.grandparent.left.color == "Red":
                        return "Red"
                    return "Black"
                else:
                    raise Exception("Apparently this parent spawned from thin air.")

            def rotate(self, child):
                # The child's parent will now be the current node's parent!
                child.parent = self.parent
                if type(self.parent) is RedBlackTree:
                    self.parent.head = child
                elif self is self.parent.left:
                    self.parent.left = child
                elif self is self.parent.right:
                    self.parent.right = child
                # Change references to match turn direction.
                if child is self.left:
                    # Move the middle links
                    child.right, self.parent, self.left = self, child, child.right
                    # Now that the middle link has been swapped over, if it is not None, set its parent to its new parent
                    if self.left is not None:
                        self.left.parent = self
                elif child is self.right:
                    # Move the middle links
                    child.left, self.parent, self.right = self, child, child.left
                    # Now that the middle link has been swapped over, if it is not None, set its parent to its new parent
                    if self.right is not None:
                        self.right.parent = self
                else:
                    raise Exception("Attempting to rotate about an invalid node.")

            def delete(self):
                # # Return in this case only, to prevent deletion of the current node.
                # print("Treating an item of type ", type(self))
                # If the node to be deleted is childless...
                if self.right is None and self.left is None:
                    # Remove this node from its parent's connections
                    if type(self.parent) == RedBlackTree:
                        self.parent.head = None
                        side = None
                    elif self is self.parent.left:
                        self.parent.left = None
                        side = "L"
                    elif self is self.parent.right:
                        self.parent.right = None
                        side = "R"
                    else:
                        raise Exception("Not sure how this heirarchy works, seems off to me.")
                    # If the deleted node was black, you need to fix up the double black count.
                    if side is None or self.color == "Red":
                        pass
                    elif self.color == "Black":
                        self.parent.resolve_double_black(side)
                # The the node to be deleted has a single child, replace it with its single child.
                # If a double black occurs, resolve it.
                elif self.right is None and self.left is not None:
                    replacement = self.left
                    if (self.color == "Black" and replacement.color == "Red") or (
                            self.color == "Red" and replacement.color == "Black"):
                        replacement.color = "Black"
                        self.give_parent_new_child(replacement)
                    elif self.color == "Black" and replacement.color == "Black":
                        self.give_parent_new_child(replacement)
                        replacement.parent.resolve_double_black("L" if replacement is replacement.parent.left else "R")
                    else:
                        raise Exception("You have two reds in a row before a deletion, something is wrong.")
                elif self.left is None and self.right is not None:
                    replacement = self.right
                    if (self.color == "Black" and replacement.color == "Red") or (
                            self.color == "Red" and replacement.color == "Black"):
                        replacement.color = "Black"
                        self.give_parent_new_child(replacement)
                    elif self.color == "Black" and replacement.color == "Black":
                        self.give_parent_new_child(replacement)
                        replacement.parent.resolve_double_black("L" if replacement is replacement.parent.left else "R")
                    else:
                        raise Exception("You have two reds in a row before a deletion, something is wrong.")
                # If the node has two valid children,
                # replace it with its immediate successor and
                # descend until a base case.
                else:
                    replacement = self.right
                    while replacement.left is not None:
                        # print("Descending a layer!")
                        replacement = replacement.left
                    # # Print a tree to debug
                    # print("Printing now!", self, replacement)
                    # print(id(self), id(self.parent), id(self.left), id(self.right))
                    # print(id(replacement), id(replacement.parent), id(replacement.left), id(replacement.right))
                    # Swap colors
                    self.color, replacement.color = replacement.color, self.color
                    # Get requisite variables
                    self_parent, self_left, self_right = \
                        self.parent, self.left, self.right
                    replacement_parent, replacement_left, replacement_right = \
                        replacement.parent, replacement.left, replacement.right
                    # Swap out-edges for the two blobs
                    if self is not replacement.parent:
                        self.parent, self.left, self.right, replacement.parent, replacement.left, replacement.right \
                            = replacement_parent, replacement_left, replacement_right, self_parent, self_left, self_right
                    elif replacement is self.left:
                        self.parent, self.left, self.right, replacement.parent, replacement.left, replacement.right \
                            = replacement, replacement_left, replacement_right, self_parent, self, self_right
                    elif replacement is self.right:
                        self.parent, self.left, self.right, replacement.parent, replacement.left, replacement.right \
                            = replacement, replacement_left, replacement_right, self_parent, self_left, self
                    # Swap in-edges for the two blobs
                    if self.left:
                        self.left.parent = self
                    if self.right:
                        self.right.parent = self
                    if replacement.left:
                        replacement.left.parent = replacement
                    if replacement.right:
                        replacement.right.parent = replacement

                    if type(self_parent) == RedBlackTree:
                        self_parent.head = replacement
                    elif self is self_parent.left:
                        self_parent.left = replacement
                    elif self is self_parent.right:
                        self_parent.left = replacement
                    else:
                        raise Exception("Hrmm.")

                    if replacement is replacement_parent.left:
                        replacement_parent.left = self
                    elif replacement is replacement_parent.right:
                        replacement_parent.right = self
                    else:
                        pass
                    # # Print the results
                    # print(id(self), id(self.parent), id(self.left), id(self.right))
                    # print(id(replacement), id(replacement.parent), id(replacement.left), id(replacement.right))
                    # # Return in this case only, to prevent deletion of the current node.
                    # print("Deleting an item of type ", type(self))
                    # self.tree.print_tree()
                    return self.delete()
                # Splice the deleted node out from the linked list
                self.prev.next = self.next
                self.next.prev = self.prev
                # Actually delete the node to save memory.
                del self

            # A helper method to splice in new children without repeating the l/r checks.
            def give_parent_new_child(self, replacement):
                replacement.parent = self.parent
                if type(self.parent) == RedBlackTree:
                    self.parent.head = replacement
                elif self is self.parent.right:
                    self.parent.right = replacement
                elif self is self.parent.left:
                    self.parent.left = replacement
                else:
                    raise Exception("You're attempting to splice in an invalid kiddo.")

            def print_tree(self, indent=0, blacks_seen=0):
                blacks_seen = blacks_seen + (1 if self.color == "Black" else 0)
                side = "H" if type(self.parent) is RedBlackTree else "L" if self is self.parent.left else "R"
                nils_check = "; Nil at {} blacks".format(blacks_seen) if self.left is None or self.right is None else ""
                print("{}{}-{} Node, Value={}, Load={}"
                      .format("|  " * indent, side, self.color, self.value, self.load) + nils_check)
                if self.left is not None:
                    self.left.print_tree(indent + 1, blacks_seen)
                if self.right is not None:
                    self.right.print_tree(indent + 1, blacks_seen)

            def validate(self, blacks_seen=0):
                blacks_seen = blacks_seen + (1 if self.color == "Black" else 0)
                left_count = blacks_seen if self.left is None else self.left.validate(blacks_seen)
                right_count = blacks_seen if self.right is None else self.right.validate(blacks_seen)
                return True if left_count is True or right_count is True or left_count != right_count else left_count

            def get_depth(self):
                return 1 + max([0 if self.left is None else self.left.get_depth(),
                                0 if self.right is None else self.right.get_depth()])

            def resolve_double_black(self, side):
                # Case 1: Double at Root Node is handled by the Tree class.
                # Case 2: Double black, black parent, red brother, two black nephews.
                db_node, brother_node = (self.left, self.right) if side == "L" else (self.right, self.left)
                if self.color == "Black" and brother_node.color == "Red" and \
                        (brother_node.left is None or brother_node.left.color == "Black") and \
                        (brother_node.right is None or brother_node.right.color == "Black"):
                    if side == "L":
                        self.rotate(self.right)
                    elif side == "R":
                        self.rotate(self.left)
                    else:
                        raise Exception("Improper turn")
                    self.parent.color = "Black"
                    self.color = "Red"
                # Case 3: There is a series of black nodes coming off.
                db_node, brother_node = (self.left, self.right) if side == "L" else (self.right, self.left)
                if self.color == "Black" and brother_node.color == "Black" and \
                        (brother_node.left is None or brother_node.left.color == "Black") and \
                        (brother_node.right is None or brother_node.right.color == "Black"):
                    if side == "L":
                        self.right.color = "Red"
                    elif side == "R":
                        self.left.color = "Red"
                    else:
                        raise Exception("Improper turn to", side)
                    new_side = "H" if type(self.parent) is RedBlackTree else \
                        "L" if self is self.parent.left else \
                            "R" if self is self.parent.right else \
                                None
                    self.parent.resolve_double_black(new_side)
                    # In this case, the double black has been moved up and out, so no new cases need be checked.
                    return
                # Case 4: Red parent, black brother and nephews.
                db_node, brother_node = (self.left, self.right) if side == "L" else (self.right, self.left)
                if self.color == "Red" and brother_node.color == "Black" and \
                        (brother_node.left is None or brother_node.left.color == "Black") and \
                        (brother_node.right is None or brother_node.right.color == "Black"):
                    self.color = "Black"
                    brother_node.color = "Red"
                    # In this case, the double black has been fully resolved, so we can go home.
                    return
                # Case 5: Either parent, black brother, one black nephew.
                if side == "L" and self.right.color == "Black" and \
                        (self.right.right is None or self.right.right.color == "Black") and \
                        (self.right.left is not None and self.right.left.color == "Red"):
                    self.right.rotate(self.right.left)
                    self.right.color = "Black"
                    self.right.right.color = "Red"
                elif side == "R" and self.left.color == "Black" and \
                        (self.left.left is None or self.left.left.color == "Black") and \
                        (self.left.right is not None and self.left.right.color == "Red"):
                    self.left.rotate(self.left.right)
                    self.left.color = "Black"
                    self.left.left.color = "Red"
                # Case 6: If the brother is black and the far nephew is red, go nuts
                if side == "L" and self.right is not None and self.right.color == "Black" and \
                        self.right.right is not None and self.right.right.color == "Red":
                    self.rotate(self.right)
                    self.parent.color = self.color
                    self.color = "Black"
                    self.parent.right.color = "Black"
                    return
                elif side == "R" and self.left is not None and self.left.color == "Black" and \
                        self.left.left is not None and self.left.left.color == "Red":
                    self.rotate(self.left)
                    self.parent.color = self.color
                    self.color = "Black"
                    self.parent.left.color = "Black"
                    return
                print("JAJAJAJAJAJAJA")

        self.NodeClass = RedBlackNode

        self.min = self.NodeClass(self, None, None)
        self.max = self.NodeClass(self, None, None)
        self.min.next = self.max
        self.max.prev = self.min

    def insert(self, v, load=None):
        self.size += 1
        # If the head is undeclared, make the head a new node.
        if self.head is None:
            self.head = self.NodeClass(self, v, load)
            self.min.next = self.head
            self.max.prev = self.head
            self.head.prev = self.min
            self.head.next = self.max
            node = self.head
        # If nodes exist, insert down into them.
        else:
            node = self.head.insert(v, load)
        # Regardless, reset the tree head to black.
        self.head.color = "Black"
        return node

    def get_depth(self):
        if self.head is None:
            return 0
        return self.head.get_depth()

    def print_tree(self):
        raise Exception()
        if self.head is None:
            print('Empty tree.')
        else:
            print("Tree contents:")
            self.head.print_tree()
        print()

    def resolve_double_black(self, side):
        self.head.color = "Black"

    def delete(self, value):
        if self.size == 0:
            raise Exception("This tree is empty. You can't delete from an empty tree.")
        else:
            curr = self.head
            done = False
            while not done:
                cmp = self.cmp(value, curr.value)
                if cmp == 1:
                    if curr.left is None:
                        raise Exception("Unable to find value to delete.")
                    else:
                        curr = curr.left
                elif cmp == -1:
                    if curr.right is None:
                        raise Exception("Unable to find value to delete.")
                    else:
                        curr = curr.right
                else:
                    done = True
            curr.delete()
        self.size -= 1
        if self.size > 0:
            self.head.color = "Black"

    def validate(self):
        if self.head is None:
            return True
        else:
            return False if self.head.validate() is True else True

    def print_list(self):
        i = 0
        curr = self.min.next
        values = []
        while curr != self.max:
            values.append((curr.value, curr.load))
            i += 1
            curr = curr.next
            if i > self.size + 5:
                raise Exception("You're iterating more times than there are items in the tree. You've fucked up.")
        print("Linked values in tree:", values)


if __name__ == "__main__":
    from random import shuffle, randint

    q = list({randint(-5000, 5000) for i in range(10)})
    tree = RedBlackTree()
    for n in q:
        print(n)
        tree.insert(n, chr(ord('a') + n % 26))
    print('q is', q, '\n')

    print("Initial tree:")
    tree.print_tree()
    tree.print_list()

    shuffle(q)

    for n in q:
        tree.delete(n)
        tree.print_list()
    print("Successfully deleted all objects.")
