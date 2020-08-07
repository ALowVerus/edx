"""
Pre-processing time: nlogn (expected)
Storage cost: n (expected)
Query time: logn (expected)
"""

import itertools
from computational_geometry.dcel import DCEL
from cs1lib import *

chain = lambda l: list(itertools.chain.from_iterable(l))


# Define a TrapezoidalMap class to manage point searches
class TrapezoidalMap(DCEL):
    def __init__(self):
        super().__init__()
        self.search_tree = self.Face(self, None)
        self.faces = {}
        self.lines = {}
        self.points = {}
        self.printed_vertices_flag = True
        self.color_index = 0
        self.line_segments_at_hand = []

    class Vertex(DCEL.Vertex):
        def __init__(self, root_map, parent, point, face):
            super().__init__((point.y, point.x))
            self.root_map = root_map
            self.parent = parent
            self.left = self.root_map.FaceNode(self.root_map, self)
            self.left.copy_values(face)
            self.left.bound_r = self
            self.right = self.root_map.FaceNode(self.root_map, self)
            self.right.copy_values(face)
            self.right.bound_l = self

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
                draw_circle(DCEL.scale_loc(self.x), DCEL.scale_loc(self.y), 5)

    class HalfEdge(DCEL.HalfEdge):
        def __init__(self, root_map, parent, source_line, face):
            self.root_map = root_map
            self.parent = parent
            self.top = self.root_map.FaceNode(self.root_map, self)
            self.top.copy_values(face)
            self.top.bound_b = self
            self.bot = self.root_map.FaceNode(self.root_map, self)
            self.bot.copy_values(face)
            self.bot.bound_t = self
            self.root_map.line_segments_at_hand.append(self)

        def propagate_new_point(self, new_point):
            if new_point.y < self.plot(new_point.x):
                self.top.propagate_new_point(new_point)
            else:
                self.bot.propagate_new_point(new_point)

        def propagate_new_line(self, new_line):
            if not (self.p0.x <= new_line.p0.x <= self.p1.x or self.p0.x <= new_line.p1.x <= self.p1.x):
                raise Exception("You've screwed up while attempting to propagate a new line.")
            bounds = sorted([self.p0.x, self.p1.x, new_line.p0.x, new_line.p1.x])
            mean_x = (bounds[1] + bounds[2]) / 2
            if self.plot(mean_x) > new_line.plot(mean_x):
                self.top.propagate_new_line(new_line)
            else:
                self.bot.propagate_new_line(new_line)

        def find_point_area(self, point):
            return (self.top if point.y < self.plot(point.x) else self.bot).find_point_area(point)

        def draw(self, part='faces'):
            self.top.draw(part)
            self.bot.draw(part)

    class Face(DCEL.Face):
        def __init__(self, root_map, parent):
            self.root_map = root_map
            self.parents = [parent]
            self.bound_l = None
            self.bound_r = None
            self.bound_t = None
            self.bound_b = None
            self.is_clicked = False

        def __str__(self):
            return str(self.vertices())

        def propagate_new_point(self, new_point):
            for parent in self.parents:
                if type(parent) is self.root_map.PointNode:
                    if self is parent.left:
                        parent.left = self.root_map.PointNode(self.root_map, parent, new_point, self)
                    elif self is parent.right:
                        parent.right = self.root_map.PointNode(self.root_map, parent, new_point, self)
                    else:
                        raise Exception("You've somehow propagated down to a badly parented point node.")
                elif type(parent) is self.root_map.LineNode:
                    if self is parent.top:
                        parent.top = self.root_map.PointNode(self.root_map, parent, new_point, self)
                    elif self is parent.bot:
                        parent.bot = self.root_map.PointNode(self.root_map, parent, new_point, self)
                    else:
                        raise Exception("You've somehow propagated down to a badly parented point node.")
                else:
                    raise Exception("You've somehow generated a FaceNode with a parent that is neither a Point nor a Line.")

        def propagate_new_line(self, new_line):
            for parent in self.parents:
                if type(parent) is self.root_map.PointNode:
                    if self is parent.left:
                        parent.left = self.root_map.LineNode(self.root_map, parent, new_line, self)
                    elif self is parent.right:
                        parent.right = self.root_map.LineNode(self.root_map, parent, new_line, self)
                    else:
                        raise Exception("You've somehow propagated down to a badly parented line node.")
                elif type(parent) is self.root_map.LineNode:
                    if self is parent.top:
                        parent.top = self.root_map.LineNode(self.root_map, parent, new_line, self)
                    elif self is parent.bot:
                        parent.bot = self.root_map.LineNode(self.root_map, parent, new_line, self)
                    else:
                        raise Exception("You've somehow propagated down to a badly parented line node.")
                else:
                    raise Exception("You've somehow generated a FaceNode with a parent that is neither a Point nor a Line.")

        @property
        def tl(self):
            return [self.bound_t.plot(self.bound_l.x) if self.bound_t else None, self.bound_l.x if self.bound_l else None]

        @property
        def bl(self):
            return [self.bound_b.plot(self.bound_l.x) if self.bound_b else None, self.bound_l.x if self.bound_l else None]

        @property
        def br(self):
            return [self.bound_b.plot(self.bound_r.x) if self.bound_b else None, self.bound_r.x if self.bound_r else None]

        @property
        def tr(self):
            return [self.bound_t.plot(self.bound_r.x) if self.bound_t else None, self.bound_r.x if self.bound_r else None]

        def vertices(self):
            return [self.tl, self.bl, self.br, self.tr]

        def copy_values(self, face):
            self.bound_l = face.bound_l
            self.bound_r = face.bound_r
            self.bound_t = face.bound_t
            self.bound_b = face.bound_b

        def find_point_area(self, point):
            return self

        def draw(self, part='faces'):
            if part == 'faces':
                # Get initial vertices
                vertices = self.vertices()
                # Account for Nones when needed. Order is TL, BL, BR, TR
                for i in [0, 3]:
                    if vertices[i][0] is None:
                        vertices[i][0] = 0
                for i in [0, 1]:
                    if vertices[i][1] is None:
                        vertices[i][1] = 0
                for i in [1, 2]:
                    if vertices[i][0] is None:
                        vertices[i][0] = DCEL.wh_n
                for i in [2, 3]:
                    if vertices[i][1] is None:
                        vertices[i][1] = DCEL.wh_n
                # Print vertices for reference.
                if self.root_map.printed_vertices_flag is True:
                    print(vertices)
                # Actually draw the polygon.
                if self.is_clicked:
                    set_fill_color(0, 0, 0)
                else:
                    r, g, b = self.color
                    set_fill_color(r, g, b)
                draw_polygon([[DCEL.scale_loc(n) for n in v][::-1] for v in vertices])

    def add_point(self, point):
        # If point is not in the map yet, add process it.
        if str(point) not in self.points:
            # Add the point to map's points
            self.points[str(point)] = []
            # If we are initializing the tree, set the first point as the root node
            if type(self.search_tree) is self.Face:
                self.search_tree = self.Vertex(self, None, point, self.search_tree)
            # If stuff exists in the tree, propagate.
            else:
                self.search_tree.propagate_new_point(point)

    def add_line_segment(self, source_line):
        if str(source_line) not in self.lines:
            for point in source_line.points:
                self.add_point(point)
            # Propagate! You can evade checks because points must necessarily already be in the tree
            if type(self.search_tree) == self.Face:
                raise Exception("You've attempted to propagate down a FaceNode. Something has gone wrong.")
            else:
                print('Now adding line {}.'.format(str(source_line)))
                # Add the line to map's lines
                self.lines[str(source_line)] = []
                # Initialize a structure to contain a list of all intersected areas.
                self.line_segments_at_hand = []
                # Propagate a search, thereby filling the areas_intersected structure.
                self.search_tree.propagate_new_line(source_line)
                # Merge generated area partitions if possible. Make sure not to screw up your object pointers.
                print('The line segments generated by this search were:')
                for line_segment in self.line_segments_at_hand:
                    print('\t{}; {}'.format(str(line_segment.top), str(line_segment.bot)))
                if len(self.line_segments_at_hand) > 1:
                    # Check the top splits
                    last_segment = self.line_segments_at_hand[0]
                    for curr_segment in self.line_segments_at_hand[1:]:
                        # If any given segment's top part's top bound matches its neighbor's top part's top bound...
                        if type(last_segment) == type(curr_segment) == self.Face \
                                and last_segment.top.bound_t is curr_segment.top.bound_t:
                            # Set the last segment's top area's bounds to encompass the current segment's area
                            last_segment.top.bound_l = curr_segment.top.bound_l
                            # Add the current segment to the last segment's area's list of parents
                            last_segment.top.parents.append(curr_segment)
                            # Set set the current segment's top to link to the new, updated last segment's top
                            curr_segment.top = last_segment.top
                        last_segment = curr_segment
                    # Check the bot splits
                    last_segment = self.line_segments_at_hand[0]
                    for curr_segment in self.line_segments_at_hand[1:]:
                        # If any given segment's bot part's bot bound matches its neighbor's bot part's bot bound...
                        if type(last_segment) == type(curr_segment) == self.Face \
                                and last_segment.bot.bound_b is curr_segment.bot.bound_b:
                            # Set the last segment's bot area's bounds to encompass the current segment's area
                            last_segment.bot.bound_l = curr_segment.bot.bound_l
                            # Add the current segment to the last segment's area's list of parents
                            last_segment.bot.parents.append(curr_segment)
                            # Set set the current segment's bot to link to the new, updated last segment's bot
                            curr_segment.bot = last_segment.bot
                        last_segment = curr_segment

    def add_face(self, f):
        points = [TrapezoidalMap.Vertex((y, x)) for y, x in f]
        lines = [TrapezoidalMap.generate_half_edge_pair(points[i], points[(i + 1) % len(points)]) for i in range(len(points))]
        for line in lines:
            self.add_line_segment(line)

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


if __name__ == "__main__":
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

    test_case = "triangle"
    if test_case == "triangle":
        points = [(1, 6), (2, 2), (3, 4)]
    elif test_case == "star":
        points = [
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
    else:
        raise Exception("You have selected an invalid test case.")

    trap_map = TrapezoidalMap()
    trap_map.add_face(points)
    print('Spawn lines have been added to the Trapezoidal Map.')


    def click(x, y):
        trap_map.click(DCEL.Vertex((DCEL.descale_loc(y), DCEL.descale_loc(x))))


    def unclick(x, y):
        pass


    def draw():
        clear()
        trap_map.draw()


    DCEL.line_side_offset = 5
    DCEL.end_shortening = 20
    DCEL.wh_pixels = 800
    DCEL.adj = 100
    min_y, min_x = min([y for y, x in points]), min([x for y, x in points])
    max_y, max_x = max([y for y, x in points]), max([x for y, x in points])
    DCEL.wh_n = max([y for y, x in points] + [x for x, y in points])
    print("MinY, MinX, MaxY, MaxX", min_y, min_x, max_y, max_x, DCEL.wh_n)
    DCEL.readjust()

    print("Commencing draw operations.")
    start_graphics(draw, width=DCEL.wh_pixels, height=DCEL.wh_pixels, mouse_press=click, mouse_release=unclick)
