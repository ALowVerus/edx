"""
Pre-processing time: nlogn (expected)
Storage cost: n (expected)
Query time: logn (expected)
"""

import itertools
from computational_geometry.drawing_lib import *
from computational_geometry.dcel import DCEL
import random

chain = lambda l: list(itertools.chain.from_iterable(l))


# Define a TrapezoidalMap class to manage point searches
class TrapezoidalMap:
    def __init__(self):

        root_map = self
        self.face_count = 0
        self.min_x, self.max_x, self.min_y, self.max_y = 0, 0, wh_n, wh_n

        class PointNode(Point):
            def __init__(self, parent, point, face):
                print("Generating a PointNode.")
                super().__init__(point.y, point.x)
                self.parent = parent
                # Create two copies of the split face
                self.left = root_map.FaceNode(self)
                self.left.copy_bounds(face)
                self.left.side_pointer_l = face.side_pointer_l
                self.right = root_map.FaceNode(self)
                self.right.copy_bounds(face)
                self.right.side_pointer_r = face.side_pointer_r
                # Edit the copies so that they refer to separate sides
                lr, rl = DCEL.HalfEdge(), DCEL.HalfEdge()
                lr.twin, rl.twin = rl, lr
                lr.face, rl.face = self.left, self.right
                self.left.bound_r = self
                self.right.bound_l = self
                DCEL.HalfEdge.splice_in_after(self.left.side_pointer_r, lr)
                DCEL.HalfEdge.splice_in_after(self.right.side_pointer_l, rl)
                # Re-assign all edges linking to the now-defunct face
                for half_edge in self.left.border_l:
                    print('L', id(half_edge))
                    half_edge.face = self.left
                for half_edge in self.right.border_r:
                    print('R', id(half_edge))
                    half_edge.face = self.right
                # Delete the defunct face
                del face

            def __str__(self):
                return "Point: ({}, {})".format(self.y, self.x)

            def propagate_new_point(self, new_point):
                if new_point.x > self.x or (new_point.x == self.x and new_point.y > self.y):
                    self.right.propagate_new_point(new_point)
                else:
                    self.left.propagate_new_point(new_point)

            def propagate_new_line(self, new_line):
                if self.x < new_line.p1.x:
                    self.right.propagate_new_line(new_line)
                if self.x > new_line.p0.x:
                    self.left.propagate_new_line(new_line)

            def find_point_area(self, point):
                return (self.right if (point.x > self.x or (point.x == self.x and point.y > self.y)) else self.left).find_point_area(point)

            def draw(self, part='faces'):
                self.right.draw(part)
                self.left.draw(part)
                if part == 'points':
                    set_fill_color(0, 0, 0)
                    draw_circle(scale_loc(self.x), scale_loc(self.y), 5)

            def print(self, indent=0):
                print(' |' * indent, str(self))
                self.left.print(indent + 1)
                self.right.print(indent + 1)

        class LineNode(Line):
            def __init__(self, parent, source_line, face):
                super().__init__(source_line.p0, source_line.p1)
                self.parent = parent
                self.top = root_map.FaceNode(self)
                self.top.copy_bounds(face)
                self.top.bound_b = self
                self.bot = root_map.FaceNode(self)
                self.bot.copy_bounds(face)
                self.bot.bound_t = self
                source_face_border_l = face.border_l
                source_face_border_r = face.border_r
                l_borders_above_line = [e for e in source_face_border_l
                                        if LineNode.compare_two_lines(e.face.bound_t, self)
                                        and LineNode.compare_two_lines(e.face.bound_b, self)]
                l_borders_inter_line = [e for e in source_face_border_l
                                        if LineNode.compare_two_lines(e.face.bound_t, self)
                                        and not LineNode.compare_two_lines(e.face.bound_b, self)]
                l_borders_below_line = [e for e in source_face_border_l
                                        if not LineNode.compare_two_lines(e.face.bound_t, self)
                                        and not LineNode.compare_two_lines(e.face.bound_b, self)]
                r_borders_above_line = [e for e in source_face_border_r
                                        if LineNode.compare_two_lines(e.face.bound_t, self)
                                        and LineNode.compare_two_lines(e.face.bound_b, self)]
                r_borders_inter_line = [e for e in source_face_border_r
                                        if LineNode.compare_two_lines(e.face.bound_t, self)
                                        and not LineNode.compare_two_lines(e.face.bound_b, self)]
                r_borders_below_line = [e for e in source_face_border_r
                                        if not LineNode.compare_two_lines(e.face.bound_t, self)
                                        and not LineNode.compare_two_lines(e.face.bound_b, self)]
                print('l_above:', l_borders_above_line)
                print('l_inter:', l_borders_inter_line)
                print('l_below:', l_borders_below_line)
                print('r_above:', r_borders_above_line)
                print('r_inter:', r_borders_inter_line)
                print('r_below:', r_borders_below_line)
                if len(l_borders_inter_line) == 0:
                    pass
                elif len(l_borders_inter_line) == 1:
                    pass
                else:
                    raise Exception("You can't have your line intersecting multiple left borders. That's impossible.")
                if len(r_borders_inter_line) == 0:
                    pass
                elif len(r_borders_inter_line) == 1:
                    pass
                else:
                    raise Exception("You can't have your line intersecting multiple left borders. That's impossible.")
                print('top_border_l', self.top.border_l)
                print('top_border_r', self.top.border_r)
                print('bot_border_l', self.bot.border_l)
                print('bot_border_r', self.bot.border_r)
                print('source_border_l', face.border_l)
                print('source_border_r', face.border_r)
                input('Hello!')
                trap_map.faces_above_added_line.append(self.top)
                trap_map.faces_below_added_line.append(self.bot)

            def __str__(self):
                return "Line: [({}, {}), ({}, {})]".format(self.p0.y, self.p0.x, self.p1.y, self.p1.x)

            @classmethod
            def compare_two_lines(cls, a, b):
                print(str(a.p0), str(a.p1), str(b.p0), str(b.p1))
                a_is_top = a.p0.y == 'Top' and a.p1.y == 'Top'
                a_is_bot = a.p0.y == 'Bot' and a.p1.y == 'Bot'
                b_is_top = b.p0.y == 'Top' and b.p1.y == 'Top'
                b_is_bot = b.p0.y == 'Bot' and b.p1.y == 'Bot'
                if a_is_top and b_is_top:
                    raise Exception("Both compared edges are tops.")
                elif a_is_bot and b_is_bot:
                    raise Exception("Both compared edges are bots.")
                elif a_is_top or b_is_bot:
                    return True
                elif a_is_bot or b_is_top:
                    return False
                elif not (a.p0.x <= b.p0.x <= a.p1.x or a.p0.x <= b.p1.x <= a.p1.x):
                    raise Exception("You've screwed up while attempting to propagate a new line.")
                bounds = sorted([a.p0.x, a.p1.x, b.p0.x, b.p1.x])
                mean_x = (bounds[1] + bounds[2]) / 2
                if a.plot(mean_x) > b.plot(mean_x):
                    return True
                else:
                    return False

            def propagate_new_point(self, new_point):
                if new_point.y < self.plot(new_point.x):
                    self.top.propagate_new_point(new_point)
                else:
                    self.bot.propagate_new_point(new_point)

            def propagate_new_line(self, new_line):
                if LineNode.compare_two_lines(self, new_line):
                    self.top.propagate_new_line(new_line)
                else:
                    self.bot.propagate_new_line(new_line)

            def find_point_area(self, point):
                return (self.top if point.y < self.plot(point.x) else self.bot).find_point_area(point)

            def draw(self, part='faces'):
                self.top.draw(part)
                self.bot.draw(part)

            def print(self, indent=0):
                print(' |' * indent, str(self))
                self.top.print(indent + 1)
                self.bot.print(indent + 1)

        class FaceNode:
            def __init__(self, parent):
                self.face_number = root_map.face_count
                root_map.face_count += 1
                self.parents = [parent]
                self.bound_l = None
                self.bound_r = None
                self.bound_t = None
                self.bound_b = None
                self.side_pointer_l = DCEL.HalfEdge()
                self.side_pointer_r = DCEL.HalfEdge()
                self.side_pointer_l.pred, self.side_pointer_l.succ = self.side_pointer_l, self.side_pointer_l
                self.side_pointer_r.pred, self.side_pointer_r.succ = self.side_pointer_r, self.side_pointer_r
                self.is_clicked = False
                self.color = (random.random(), random.random(), random.random())

            def __str__(self):
                return "Face: {}, left_#s: {}, right_#s: {}".format(
                    self.face_number,
                    [e.twin.face.face_number for e in self.border_l],
                    [e.twin.face.face_number for e in self.border_r])

            def propagate_new_point(self, new_point):
                for parent in self.parents:
                    if type(parent) is root_map.PointNode:
                        if self is parent.left:
                            parent.left = root_map.PointNode(parent, new_point, self)
                        elif self is parent.right:
                            parent.right = root_map.PointNode(parent, new_point, self)
                        else:
                            raise Exception("You've somehow propagated down to a badly parented point node.")
                    elif type(parent) is root_map.LineNode:
                        if self is parent.top:
                            parent.top = root_map.PointNode(parent, new_point, self)
                        elif self is parent.bot:
                            parent.bot = root_map.PointNode(parent, new_point, self)
                        else:
                            raise Exception("You've somehow propagated down to a badly parented point node.")
                    else:
                        raise Exception("You've somehow generated a FaceNode with a parent that is neither a Point nor a Line.")

            def propagate_new_line(self, new_line):
                for parent in self.parents:
                    if type(parent) is root_map.PointNode:
                        if self is parent.left:
                            parent.left = root_map.LineNode(parent, new_line, self)
                        elif self is parent.right:
                            parent.right = root_map.LineNode(parent, new_line, self)
                        else:
                            raise Exception("You've somehow propagated down to a badly parented line node.")
                    elif type(parent) is root_map.LineNode:
                        if self is parent.top:
                            parent.top = root_map.LineNode(parent, new_line, self)
                        elif self is parent.bot:
                            parent.bot = root_map.LineNode(parent, new_line, self)
                        else:
                            raise Exception("You've somehow propagated down to a badly parented line node.")
                    else:
                        raise Exception("You've somehow generated a FaceNode with a parent that is neither a Point nor a Line.")

            @classmethod
            def get_side_border(cls, pointer):
                curr = pointer.succ
                border = []
                while curr.face is not None:
                    border.append(curr)
                    curr = curr.succ
                return border

            @property
            def border_l(self):
                return FaceNode.get_side_border(self.side_pointer_l)

            @property
            def border_r(self):
                return FaceNode.get_side_border(self.side_pointer_r)

            @property
            def tl(self):
                return [self.bound_t.plot(self.bound_l.x) if self.bound_t else None,
                        self.bound_l.x if self.bound_l else None]

            @property
            def bl(self):
                return [self.bound_b.plot(self.bound_l.x) if self.bound_b else None,
                        self.bound_l.x if self.bound_l else None]

            @property
            def br(self):
                return [self.bound_b.plot(self.bound_r.x) if self.bound_b else None,
                        self.bound_r.x if self.bound_r else None]

            @property
            def tr(self):
                return [self.bound_t.plot(self.bound_r.x) if self.bound_t else None,
                        self.bound_r.x if self.bound_r else None]

            def vertices(self):
                return [self.tl, self.bl, self.br, self.tr]

            def copy_bounds(self, face):
                self.bound_l = face.bound_l
                self.bound_r = face.bound_r
                self.bound_t = face.bound_t
                self.bound_b = face.bound_b

            def find_point_area(self, point):
                return self

            def draw(self, part='faces'):
                if part == 'faces':
                    # Get initial vertices
                    vertices = [((0 if y == 'Top' else wh_n if y == 'Bot' else y),
                                 (0 if x == 'Left' else wh_n if x == 'Right' else x))
                                for y, x in self.vertices()]
                    # Print vertices for reference.
                    if root_map.printed_vertices_flag is True:
                        print(vertices)
                    # Actually draw the polygon.
                    if self.is_clicked:
                        set_fill_color(0, 0, 0)
                    else:
                        r, g, b = self.color
                        set_fill_color(r, g, b)
                    draw_polygon([[scale_loc(n) for n in v][::-1] for v in vertices])
                    y, x = min(vertices)
                    set_stroke_color(0, 0, 0)
                    draw_text(str(self.face_number), scale_loc(x) + 20, scale_loc(y) + 20)

            def print(self, indent=0):
                print(' |' * indent, str(self))

        self.PointNode = PointNode
        self.LineNode = LineNode
        self.FaceNode = FaceNode

        self.search_tree = self.FaceNode(None)
        self.search_tree.bound_t = Line(('Top', 'Left'), ('Top', 'Right'))
        self.search_tree.bound_b = Line(('Bot', 'Left'), ('Bot', 'Right'))
        self.search_tree.bound_l = Point("Top", "Left")
        self.search_tree.bound_r = Point("Top", "Right")
        self.faces = {}
        self.lines = {}
        self.points = {}
        self.printed_vertices_flag = True
        self.faces_above_added_line = []
        self.faces_below_added_line = []

    def add_point(self, point):
        # If point is not in the map yet, add process it.
        if str(point) not in self.points:
            # Add the point to map's points
            self.points[str(point)] = []
            # If we are initializing the tree, set the first point as the root node
            if type(self.search_tree) is self.FaceNode:
                self.search_tree = self.PointNode(None, point, self.search_tree)
            # If stuff exists in the tree, propagate.
            else:
                self.search_tree.propagate_new_point(point)

    def add_line_segment(self, source_line):
        if str(source_line) not in self.lines:
            for point in source_line.points:
                self.add_point(point)
                run()
            # Propagate! You can evade checks because points must necessarily already be in the tree
            if type(self.search_tree) == self.FaceNode:
                raise Exception("You've attempted to propagate down a FaceNode. Something has gone wrong.")
            else:
                print('Now adding line {}.'.format(str(source_line)))
                # Add the line to map's lines
                self.lines[str(source_line)] = []
                # Initialize a structure to contain a list of all intersected areas.
                self.faces_above_added_line = []
                self.faces_below_added_line = []
                # Propagate a search, thereby filling the areas_intersected structure.
                self.search_tree.propagate_new_line(source_line)
                # Merge generated area partitions if possible. Make sure not to screw up your object pointers.
                print('The faces split above the added line are:')
                for face in self.faces_above_added_line:
                    print('\t{}'.format(str(face)))
                print('The faces split below the added line are:')
                for face in self.faces_below_added_line:
                    print('\t{}'.format(str(face)))
                # if len(self.faces_above_added_line) > 1:
                #     print("There are multiple split faces.")
                #     for adjacent_face_list in [self.faces_above_added_line, self.faces_below_added_line]:
                #         # Check the top splits
                #         last_face = adjacent_face_list[0]
                #         for curr_face in adjacent_face_list[1:]:
                #             # If any given segment's top part's top bound matches its neighbor's top part's top bound...
                #             if type(last_face) == type(curr_face) == self.FaceNode \
                #                     and last_face.top.bound_t is curr_face.top.bound_t \
                #                     and last_face.bot.bound_b is curr_face.bot.bound_b:
                #                 # Set the last segment's top area's bounds to encompass the current segment's area
                #                 last_face.top.bound_r = curr_face.top.bound_r
                #                 # Add the current segment to the last segment's area's list of parents
                #                 last_face.top.parents.append(curr_face)
                #                 # Set set the current segment's top to link to the new, updated last segment's top
                #                 curr_face.top = last_face.top
                #             last_face = curr_face
            run()

    def add_segments_from_coord_list(self, coord_list):
        points = [Point(y, x) for y, x in coord_list]
        lines = [Line(points[i], points[(i + 1) % len(points)]) for i in range(len(points) - 1)]
        for line in lines:
            self.add_line_segment(line)

    def add_face(self, coord_list):
        self.add_segments_from_coord_list(coord_list + coord_list[:1])

    def remove_face(self, f):
        pass

    def find_point_area(self, point):
        return self.search_tree.find_point_area(point)

    def click(self, point):
        area = self.find_point_area(point)
        area.is_clicked = not area.is_clicked

    def draw(self):
        self.color_index = 0
        self.search_tree.draw('faces')
        self.search_tree.draw('points')
        self.printed_vertices_flag = False

    def print(self):
        print()
        self.search_tree.print()
        print()

# # Start with a list of points
# seeds = [Point(y, x) for y, x in set([(randint(0, wh_n), randint(0, wh_n)) for i in range(30)])]
# print(', '.join([str(s) for s in seeds]))
# def draw():
#     clear()
#     set_fill_color(0, 0, 0)
#     set_stroke_color(0, 0, 0)
#     for p in seeds:
#         draw_circle(p.x * scalar + adj, p.y * scalar + adj, 3)


print('Lines have been defined.')

trap_map = TrapezoidalMap()
line = [(1, 6), (2, 2)]
triangle = [(1, 6), (2, 2), (3, 4)][::-1]
star = [
    (2.4, 3.5),
    (0.5, 4),
    (2, 2.5),
    (1, 1),
    (3, 2),
    (5, 1),
    (4, 2.5),
    (5.5, 4),
    (3.6, 3.5),
    (3, 5.7),
][:3]


def click(x, y):
    trap_map.click(Point(descale_loc(y), descale_loc(x)))


def unclick(x, y):
    pass


def draw():
    clear()
    trap_map.draw()


def run():
    print("Commencing draw operations.")
    trap_map.print()
    start_graphics(draw, width=wh_pixels, height=wh_pixels, mouse_press=click, mouse_release=unclick)


trap_map.add_face(triangle)
# trap_map.add_segments_from_coord_list(line)
trap_map.print()
print('Spawn lines have been added to the Trapezoidal Map.')
