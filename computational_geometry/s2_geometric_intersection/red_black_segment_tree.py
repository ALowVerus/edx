from computational_geometry.s2_geometric_intersection.line_helper_functions import *
from math import atan2


# Initialize a structure to hold the currently-valid line segments
class RedBlackSegmentTree:
    def __init__(self):
        self.head = None
        self.size = 0
        self.min = RedBlackSegmentTree.RedBlackNode(self, None)
        self.max = RedBlackSegmentTree.RedBlackNode(self, None)
        self.min.next = self.max
        self.max.prev = self.min
        self.segment_to_node = {}

    def insert(self, seg, x):
        self.size += 1
        # If the head is undeclared, make the head a new node.
        if self.head is None:
            self.head = RedBlackSegmentTree.RedBlackNode(self, seg)
            self.segment_to_node[seg] = self.head
            self.min.next = self.head
            self.max.prev = self.head
            self.head.prev = self.min
            self.head.next = self.max
            new_intersection_points = []
        # If nodes exist, insert down into them.
        else:
            new_intersection_points, node_reference = self.head.insert(seg, x)
            self.segment_to_node[seg] = node_reference
        # Regardless, reset the tree head to black.
        self.head.color = "Black"
        return new_intersection_points

    def find_nearest(self, p):
        if self.size is 0:
            raise Exception("Ya done goofed. There are no nearest items to a target when considering an empty tree.")
        return self.head.find_nearest(p)

    def get_depth(self):
        if self.head is None:
            return 0
        return self.head.get_depth()

    def print_tree(self):
        if self.head is None:
            print('Empty tree.')
        else:
            print("Tree contents:")
            self.head.print_tree()

    def resolve_double_black(self, side):
        self.head.color = "Black"

    def delete(self, seg, x):
        print('Subtracting from size.')
        if self.size <= 0:
            raise Exception("This tree is empty. You can't delete from an empty tree.")
        self.size -= 1
        print("Removing segment", seg)
        node_of_seg = self.segment_to_node[seg]
        print('The associated node contains', node_of_seg.segments)
        node_of_seg.segments.remove(seg)
        self.segment_to_node.pop(seg, None)
        new_intersections = []
        if len(node_of_seg.segments) == 0:
            if node_of_seg.prev.std_form is not None and node_of_seg.next.std_form is not None:
                new_intersection = check_intersection(node_of_seg.prev.segments[0], node_of_seg.next.segments[0])
                if len(new_intersection) == 1 \
                        and len(new_intersection[0][2]) == 1 \
                        and new_intersection[0][2][0][0] > x:
                    new_intersections.extend(new_intersection)
            node_of_seg.delete()
        if self.head is not None:
            self.head.color = "Black"
        return new_intersections

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
            values.append(curr.segments)
            i += 1
            curr = curr.next
            if i > self.size + 5:
                raise Exception("You're more items than there are in the tree. Impossible. List: {}".format(values))
        print("Linked values in tree:", values)

    class RedBlackNode:
        def __init__(self, parent, seg):
            self.color = 'Red'
            self.parent = parent
            self.segments = [seg]
            self.std_form = std_form_seg(seg) if seg is not None else None
            self.angle = atan2(seg[1][1]-seg[0][1], seg[1][0]-seg[0][0]) if seg is not None else None
            self.left = None
            self.right = None
            self.prev = None
            self.next = None

        def plot(self, x):
            A, B, C = self.std_form
            return (C - A * x) / B

        def insert(self, seg, x):
            cmp_value = cmp_std_forms_at_x(std_form_seg(seg), self.std_form, x)
            if cmp_value < 0:
                if self.left is not None:
                    return self.left.insert(seg, x)
                else:
                    self.left = RedBlackSegmentTree.RedBlackNode(self, seg)
                    self.left.prev = self.prev
                    self.left.prev.next = self.left
                    self.prev = self.left
                    self.left.next = self
                    new_intersections = self.left.predict_intersection_points(x)
                    self.left.resolve_conflicts()
                    return new_intersections, self.left
            elif cmp_value > 0:
                if self.right is not None:
                    return self.right.insert(seg, x)
                else:
                    self.right = RedBlackSegmentTree.RedBlackNode(self, seg)
                    self.right.next = self.next
                    self.right.next.prev = self.right
                    self.next = self.right
                    self.right.prev = self
                    new_intersections = self.right.predict_intersection_points(x)
                    self.right.resolve_conflicts()
                    return new_intersections, self.right
            else:
                self.segments.append(seg)
                return [], self

        def predict_intersection_points(self, x):
            potential_intersections = []
            if self.prev.std_form is not None:
                prev_hit = check_intersection(self.segments[0], self.prev.segments[0])
                if len(prev_hit) == 1 and len(prev_hit[0][2]) == 1:
                    potential_intersections.extend(prev_hit)
            if self.next.std_form is not None:
                next_hit = check_intersection(self.segments[0], self.next.segments[0])
                if len(next_hit) == 1 and len(next_hit[0][2]) == 1:
                    potential_intersections.extend(next_hit)
            return [item[2][0] for item in potential_intersections]

        def resolve_conflicts(self):
            # If grandparents do not exist, you've reached the end.
            if type(self.parent) is RedBlackSegmentTree or type(self.parent.parent) is RedBlackSegmentTree:
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
            if type(self.parent) is RedBlackSegmentTree:
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

        def find_nearest(self, p):
            y = self.plot(p[0])
            if y < p[1]:
                if self.left is not None:
                    return self.left.find_nearest(p)
                else:
                    return self
            elif y > p[1]:
                if self.right is not None:
                    return self.right.find_nearest(p)
                else:
                    return self
            else:
                return self

        def delete(self):
            # If the node to be deleted is childless...
            if self.right is None and self.left is None:
                # Remove this node from its parent's connections
                if type(self.parent) is RedBlackSegmentTree:
                    self.parent.head = None
                    side = None
                elif self is self.parent.left:
                    self.parent.left = None
                    side = "L"
                elif self is self.parent.right:
                    self.parent.right = None
                    side = "R"
                else:
                    raise Exception("Not sure how this heirarchy works, seems off to me.", id(self), id(self.parent), id(self.parent.right), id(self.parent.left))
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
            # If the node has two valid children, replace it with its immediate successor and descend until a base case.
            else:
                replacement = self.right
                while replacement.left is not None:
                    replacement = replacement.left
                RedBlackSegmentTree.RedBlackNode.swap_node_connections(self, replacement)
                self.delete()
                # Return in this case only, to prevent deletion of the current node.
                return
            # Splice the deleted node out from the linked list
            self.prev.next = self.next
            self.next.prev = self.prev
            # Actually delete the node to save memory.
            del self

        # A method to replace one node with another in the tree.
        @classmethod
        def swap_node_connections(cls, a, b):
            print("Swapping {} and {}".format(id(a), id(b)))
            root = a.parent
            while type(root) is not RedBlackSegmentTree:
                root = root.parent
            root.print_tree()
            # Swap innocent items
            a.color, b.color = b.color, a.color
            # Handle linked list references
            if a.next is b:
                a.next = b.next
                b.prev = a.prev
                a.prev = b
                b.next = a
            elif b.next is a:
                b.next = a.next
                a.prev = b.prev
                b.prev = a
                a.next = b
            else:
                a.prev, b.prev = b.prev, a.prev
                a.next, b.next = b.next, a.next
            a.prev.next = a
            a.next.prev = a
            b.prev.next = b
            b.next.prev = b
            # Handle family references
            if a is b.parent:
                a_left_o, a_right_o = a.left, a.right
                a.left, a.right = b.left, b.right
                if a.left is not None:
                    a.left.parent = a
                if a.right is not None:
                    a.right.parent = a
                b.parent = a.parent
                a.parent = b
                if type(b.parent) is RedBlackSegmentTree:
                    b.parent.head = b
                elif b.parent.right is a:
                    b.parent.right = b
                elif b.parent.left is a:
                    b.parent.left = b
                if b is a_right_o:
                    b.right = a
                    b.left = a_left_o
                    if b.left is not None:
                        b.left.parent = b
                elif b is a_left_o:
                    b.left = a
                    b.right = a_right_o
                    if b.right is not None:
                        b.right.parent = b
                else:
                    raise Exception("Failure. A is B's parent, but neither of B's children are A.")
            elif b is a.parent:
                b_left_o, b_right_o = b.left, b.right
                b.left, b.right = a.left, a.right
                if b.left is not None:
                    b.left.parent = b
                if b.right is not None:
                    b.right.parent = b
                a.parent = b.parent
                b.parent = a
                if type(a.parent) is RedBlackSegmentTree:
                    a.parent.head = a
                elif a.parent.right is b:
                    a.parent.right = a
                elif a.parent.left is b:
                    a.parent.left = a
                if a is b_right_o:
                    a.right = b
                    a.left = b_left_o
                    if a.left is not None:
                        a.left.parent = a
                elif a is b_left_o:
                    a.left = b
                    a.right = b_right_o
                    if a.right is not None:
                        a.right.parent = a
                else:
                    raise Exception("Failure. B is A's parent, but neither of A's children are B.")
            else:
                # Swap sideways connections
                a.right, b.right = b.right, a.right
                a.left, b.left = b.left, a.left
                a.parent, b.parent = b.parent, a.parent
                # Fix up connected children
                if a.right is not None:
                    a.right.parent = a
                if a.left is not None:
                    a.left.parent = a
                if b.right is not None:
                    b.right.parent = b
                if b.left is not None:
                    b.left.parent = b
                # Fix up connected parents
                if type(a.parent) is RedBlackSegmentTree:
                    a.parent.head = a
                elif a.parent.right is b:
                    a.parent.right = a
                elif a.parent.left is b:
                    a.parent.left = a
                if type(b.parent) is RedBlackSegmentTree:
                    b.parent.head = b
                elif b.parent.right is a:
                    b.parent.right = b
                elif b.parent.left is a:
                    b.parent.left = b
            root.print_tree()

        # A helper method to splice in new children without repeating the l/r checks.
        def give_parent_new_child(self, replacement):
            replacement.parent = self.parent
            if type(self.parent) == RedBlackSegmentTree:
                self.parent.head = replacement
            elif self is self.parent.right:
                self.parent.right = replacement
            elif self is self.parent.left:
                self.parent.left = replacement
            else:
                raise Exception("You're attempting to splice in an invalid kiddo.")

        def print_tree(self, indent=0, blacks_seen=0):
            blacks_seen = blacks_seen + (1 if self.color == "Black" else 0)
            side = "H" if type(self.parent) is RedBlackSegmentTree else "L" if self is self.parent.left else "R"
            nils_check = "; Nil at {} blacks".format(blacks_seen) if self.left is None or self.right is None else ""
            print("{}{}-{} Node, Value={}".format("|  " * indent, side, self.color, self.segments) + nils_check)
            if type(self.parent) is RedBlackSegmentTree:
                does_match = id(self.parent.head) == id(self)
                print("{}T:{}, {}, {}, {}".format("   " * indent, id(self), id(self.parent), id(self.parent.head), does_match))
            else:
                does_match = (id(self) == id(self.parent.left) and id(self) != id(self.parent.right)) or \
                             (id(self) != id(self.parent.left) and id(self) == id(self.parent.right))
                print("{}T:{}, {}, {}, {}, {}".format("   " * indent, id(self), id(self.parent), id(self.parent.left), id(self.parent.right), does_match))
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
            if self.color is "Black" and brother_node.color is "Red" and \
                    (brother_node.left is None or brother_node.left.color == "Black") and \
                    (brother_node.right is None or brother_node.right.color == "Black"):
                if side is "L":
                    self.rotate(self.right)
                elif side is "R":
                    self.rotate(self.left)
                else:
                    raise Exception("Improper turn")
                self.parent.color = "Black"
                self.color = "Red"
            # Case 3: There is a series of black nodes coming off.
            db_node, brother_node = (self.left, self.right) if side == "L" else (self.right, self.left)
            if self.color is "Black" and brother_node.color is "Black" and \
                    (brother_node.left is None or brother_node.left.color == "Black") and \
                    (brother_node.right is None or brother_node.right.color == "Black"):
                if side is "L":
                    self.right.color = "Red"
                elif side is "R":
                    self.left.color = "Red"
                else:
                    raise Exception("Improper turn to", side)
                new_side = "H" if type(self.parent) is RedBlackSegmentTree else \
                    "L" if self is self.parent.left else \
                        "R" if self is self.parent.right else \
                            None
                self.parent.resolve_double_black(new_side)
                # In this case, the double black has been moved up and out, so no new cases need be checked.
                return
            # Case 4: Red parent, black brother and nephews.
            db_node, brother_node = (self.left, self.right) if side == "L" else (self.right, self.left)
            if self.color is "Red" and brother_node.color is "Black" and \
                    (brother_node.left is None or brother_node.left.color == "Black") and \
                    (brother_node.right is None or brother_node.right.color == "Black"):
                self.color = "Black"
                brother_node.color = "Red"
                # In this case, the double black has been fully resolved, so we can go home.
                return
            # Case 5: Either parent, black brother, one black nephew.
            if side is "L" and self.right.color is "Black" and \
                    (self.right.right is None or self.right.right.color is "Black") and \
                    (self.right.left is not None and self.right.left.color is "Red"):
                self.right.rotate(self.right.left)
                self.right.color = "Black"
                self.right.right.color = "Red"
            elif side is "R" and self.left.color is "Black" and \
                    (self.left.left is None or self.left.left.color is "Black") and \
                    (self.left.right is not None and self.left.right.color is "Red"):
                self.left.rotate(self.left.right)
                self.left.color = "Black"
                self.left.left.color = "Red"
            # Case 6: If the brother is black and the far nephew is red, go nuts
            if side is "L" and self.right is not None and self.right.color is "Black" and \
                    self.right.right is not None and self.right.right.color is "Red":
                self.rotate(self.right)
                self.parent.color = self.color
                self.color = "Black"
                self.parent.right.color = "Black"
                return
            elif side is "R" and self.left is not None and self.left.color is "Black" and \
                    self.left.left is not None and self.left.left.color is "Red":
                self.rotate(self.left)
                self.parent.color = self.color
                self.color = "Black"
                self.parent.left.color = "Black"
                return
            print("JAJAJAJAJAJAJA")


if __name__ == "__main__":
    from random import shuffle

    # t = RedBlackSegmentTree()
    #
    # segments = [((0,0), (2,0)), ((0,1), (2,1)), ((0,2), (2,2)), ((0,3), (2,3))] + [((1,0.5), (3,0.5))]
    # for seg in segments:
    #     print(seg, ':::', t.insert(seg, seg[0][0]))
    # print("Final tree:")
    # t.print_tree()
    # t.print_list()
    # print()
    # shuffle(segments)
    # print(segments)
    # for seg in segments:
    #     t.delete(seg, 1)
    #     print("Removed {}".format(seg))
    #     t.print_tree()
    #     t.print_list()
    #     print()

    t = RedBlackSegmentTree()
    t.head = RedBlackSegmentTree.RedBlackNode(t, None)
    t.head.right = RedBlackSegmentTree.RedBlackNode(t.head, None)
    t.head.color = "Black"
    t.head.right.color = "Red"
    t.head.segments = "A"
    t.head.right.segments = "B"
    t.print_tree()
    print()
    t.RedBlackNode.swap_node_connections(t.head, t.head.right)
    print()
    t.print_tree()
