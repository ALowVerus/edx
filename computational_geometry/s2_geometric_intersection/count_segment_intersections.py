from computational_geometry.s2_geometric_intersection.red_black_segment_tree import *
from computational_geometry.s2_geometric_intersection.segment_event_heap import *
from cs1lib import *
from random import randint
from math import atan2


def brute_solve(s_list, r_list, l_list, c_list):
    intersections = []
    # for i in range(len(s_list)):
    #     for j in range(i + 1, len(s_list)):
    #         new_intersections = check_intersection(s_list[i], s_list[j])
    #         intersections.extend(new_intersections)
    print()
    print("Final intersections:")
    for intersection in intersections:
        print('\t', intersection)
    return intersections


# def sweepline_solve(s_list, r_list, l_list, c_list):
#     # Separate vertical lines from others, since they will break the x-based comparisons
#     verticals = [seg for seg in segments if seg[0][0] == seg[1][0]]
#     verticals_dict = {}
#     for seg in verticals:
#         if seg[0][0] not in verticals_dict:
#             verticals_dict[seg[0][0]] = []
#         verticals_dict[seg[0][0]].append(seg)
#     # Use non-vertical lines as valid entry points in the sweepline
#     segments = [seg for seg in segments if seg[0][0] != seg[1][0]]
#     # Get a queue for the start and end points of the lines, which will have to be dealt with eventually regardless
#     po_to_line = {}
#     pf_to_line = {}
#     for po, pf in segments:
#         if po not in po_to_line:
#             po_to_line[po] = []
#         po_to_line[po].append((po, pf))
#         if pf not in pf_to_line:
#             pf_to_line[pf] = []
#         pf_to_line[pf].append((po, pf))
#
#     # Initialize a queue to hold the actions as they come in
#     h = SegmentEventHeap()
#
#     # Load the heap up with the start and end points. Hash them first to remove dupes.
#     for p in {p for p in list(po_to_line.keys()) + list(pf_to_line.keys())}:
#         h.add('Point', p)
#
#     # Load the heap up with the x-coordinates of the verticals
#     for x in verticals_dict:
#         h.add('Vertical', x)
#
#     # Initialize a structure to hold the currently-valid line segments
#     t = RedBlackSegmentTree()
#
#     print(sorted(list(po_to_line.keys())))
#     print(sorted(list(pf_to_line.keys())))
#     print(sorted(list(verticals_dict.keys())))
#
#     # While there are events in the queue, keep popping!
#     intersections = []
#     while len(h.entries) > 0:
#         print()
#         curr_x = h.entries[0][0]
#         print("Intersections already hit are:")
#         for item in intersections:
#             print("    ", item)
#         print("Popping at x={}".format(curr_x))
#         t.print_tree()
#         t.print_list()
#         # Pop an item from the heap
#         points_on_x, hits_vertical = h.step()
#         print(points_on_x, hits_vertical)
#         # Add all the new lines with start points at this x to the RBTree
#         for po in points_on_x:
#             if po in po_to_line:
#                 for segment in po_to_line[po]:
#                     print("Adding new segment to the size {} tree: {}".format(t.size, segment))
#                     new_intersection_points = t.insert(segment, curr_x)
#                     print("Size is now {}.".format(t.size))
#                     for p in new_intersection_points:
#                         print("Generated new intersection point", p)
#                         if p[0] > curr_x + LEEWAY:
#                             h.add('Point', p)
#                 # Pop to prevent double adds of any given segments
#                 po_to_line.pop(po)
#         print()
#         print("After adding points for this round:")
#         t.print_tree()
#         t.print_list()
#         print("Size is", t.size)
#         # If there are verticals to deal with...
#         if curr_x in verticals_dict:
#             # Check lines currently in the RBTree against the vertical hits to find crossings
#             if t.size > 0:
#                 # For each vertical
#                 for vertical in verticals_dict[curr_x]:
#                     # Find the point closest to the target
#                     match = t.find_nearest(vertical[0])
#                     while match.std_form is not None and match.plot(x) >= vertical[0][1]:
#                         match = match.prev
#                     # Overshot, move up one
#                     match = match.next
#                     # Iterate downwards, increasing y, until going OOB, adding hit segments to the list of segments
#                     lines_between = []
#                     while match.std_form is not None and match.plot(x) <= vertical[1][1]:
#                         lines_between.append(match)
#                         match = match.next
#                     # Generate intersection objects
#                     for line in lines_between:
#                         for segment in line.segments:
#                             intersections.append([segment, vertical, [[curr_x, line.plot(curr_x)]]])
#             # Scan the verticals against each other to get segment overlaps
#             vertical_segments = sorted(verticals_dict[curr_x])
#             for i in range(len(vertical_segments)):
#                 j = i+1
#                 while j < len(vertical_segments) and vertical_segments[i][1][1] >= vertical_segments[j][0][1]:
#                     intersection = check_intersection(vertical_segments[i], vertical_segments[j])
#                     if intersection:
#                         intersections.append((vertical_segments[i], vertical_segments[j], intersection))
#                     j += 1
#         # Deal with any intersections at this x
#         # If there are items inside the line structure, check for intersections
#         if t.size > 0:
#             for pi in points_on_x:
#                 # Get to the neighborhood of the intersection
#                 curr_intersecting_line = t.find_nearest(pi)
#                 print('Intersecting line nearest to {}: {}'.format(pi, curr_intersecting_line.segments))
#                 # Get to the top line
#                 while curr_intersecting_line.std_form is not None and curr_intersecting_line.plot(pi[0]) >= pi[1] - LEEWAY:
#                     curr_intersecting_line = curr_intersecting_line.prev
#                 curr_intersecting_line = curr_intersecting_line.next
#                 print('Lowest Intersecting line hitting {}: {}'.format(pi, curr_intersecting_line.segments))
#                 # Move down until all crossing lines are enumerated
#                 crossing_lines = []
#                 while curr_intersecting_line.std_form is not None and curr_intersecting_line.plot(pi[0]) <= pi[1] + LEEWAY:
#                     crossing_lines.append(curr_intersecting_line)
#                     curr_intersecting_line = curr_intersecting_line.next
#                 # Remove invalid lines. The fact that this is required implies that the previous checks are not valid.
#                 crossing_lines = [line for line in crossing_lines if pi[1] - LEEWAY < line.plot(pi[0]) < pi[1] + LEEWAY]
#                 print('Crossing lines at {}: {}'.format(pi, [line.segments for line in crossing_lines]))
#                 # Reverse order of the crossing lines
#                 if len(crossing_lines) >= 2:
#                     print("An intersection has occurred.", pi)
#                     # Reverse the intersecting lines - after crossing a single point, they should essentially be reversed.
#                     for i in range(len(crossing_lines)//2):
#                         RedBlackSegmentTree.RedBlackNode.swap_node_connections(crossing_lines[i], crossing_lines[len(crossing_lines)-i-1])
#                     crossing_lines = crossing_lines[::-1]
#                     # Add the new front and back intersection points to the heap.
#                     if crossing_lines[0].prev.std_form is not None:
#                         bot_intersection_hits = check_intersection(crossing_lines[0].prev.segments[0], crossing_lines[0].segments[0])
#                         if len(bot_intersection_hits) == 1:
#                             bot_intersection_coords = bot_intersection_hits[0][2]
#                             if len(bot_intersection_coords) == 1:
#                                 bot_intersection_point = bot_intersection_coords[0]
#                                 if bot_intersection_point[0] > curr_x + LEEWAY:
#                                     h.add("Point", bot_intersection_point)
#                     if crossing_lines[-1].next.std_form is not None:
#                         top_intersection_hits = check_intersection(crossing_lines[-1].segments[0], crossing_lines[-1].next.segments[0])
#                         if len(top_intersection_hits) == 1:
#                             top_intersection_coords = top_intersection_hits[0][2]
#                             if len(top_intersection_coords) == 1:
#                                 top_intersection_point = top_intersection_coords[0]
#                                 if top_intersection_point[0] > curr_x + LEEWAY:
#                                     h.add("Point", top_intersection_point)
#                     # Add intersections for all lines in the crossing section, in O(n^2) time
#                     for i in range(len(crossing_lines)):
#                         for segment_i in crossing_lines[i].segments:
#                             for j in range(i+1, len(crossing_lines)):
#                                 for segment_j in crossing_lines[j].segments:
#                                     intersections.append((segment_i, segment_j, (pi,)))
#         print("After resolving intersections:")
#         t.print_tree()
#         t.print_list()
#         print()
#         # Remove all old lines with end points at this x from the RBTree
#         for pf in points_on_x:
#             if pf in pf_to_line:
#                 for segment in pf_to_line[pf]:
#                     new_intersection_points = t.delete(segment, curr_x)
#                     print(new_intersection_points)
#                     for p in [item[2][0] for item in new_intersection_points]:
#                         if p[0] > curr_x + LEEWAY:
#                             h.add('Point', p)
#                 # Pop to prevent intersections from double counting
#                 pf_to_line.pop(pf)
#         print(len(intersections))
#         print()
#         print()
#         print()
#     # Once the event heap is empty, return the result
#     print(t.size)
#     print('Final intersections:', intersections)
#     return intersections


class IntersectionFinder:

    def __init__(self, s_list, r_list, l_list, c_list):
        finder = self
        self.leeway = 0.0000001

        class LinearSegment:
            def __init__(self, x, y, u, v, t):
                if t not in 'srl':
                    raise Exception("You tried to create a LinearSegment with an improper type designation.")
                self.x, self.y, self.u, self.v, self.t = x, y, u, v, t

            def draw(self, wh, min_d, max_d):
                if self.t == 's':
                    set_stroke_color(0, 0, 0)
                    x1, y1, x2, y2 = self.x, self.y, self.u, self.v
                elif self.t == 'r':
                    set_stroke_color(1, 0, 0)
                    x1, y1, x2, y2 = self.x, self.y, self.u, self.v
                elif self.t == 'l':
                    set_stroke_color(0, 0.7, 0)
                    x1, y1, x2, y2 = self.x, self.y, self.u, self.v
                else:
                    raise Exception()
                draw_line((x1 - min_d) * wh / (max_d - min_d),
                          (y1 - min_d) * wh / (max_d - min_d),
                          (x2 - min_d) * wh / (max_d - min_d),
                          (y2 - min_d) * wh / (max_d - min_d))

            @property
            def theta(self):
                return atan2(self.v - self.y, self.u - self.x)

            @property
            def a(self):
                return self.y - self.v

            @property
            def b(self):
                return self.u - self.x

            @property
            def min_x(self):
                min_x = min([self.x, self.u])
                if self.t not in 'srl':
                    raise Exception("Invalid line type designation.")
                return min_x if (self.t == 's') or (self.t == 'r' and min_x == self.x) else None

            @property
            def min_y(self):
                min_y = min([self.y, self.v])
                if self.t not in 'srl':
                    raise Exception("Invalid line type designation.")
                return min_y if (self.t == 's') or (self.t == 'r' and min_y == self.y) else None

            @property
            def max_x(self):
                max_x = max([self.x, self.u])
                if self.t not in 'srl':
                    raise Exception("Invalid line type designation.")
                return max_x if (self.t == 's') or (self.t == 'r' and max_x == self.x) else None

            @property
            def max_y(self):
                max_y = max([self.y, self.v])
                if self.t not in 'srl':
                    raise Exception("Invalid line type designation.")
                return max_y if (self.t == 's') or (self.t == 'r' and max_y == self.y) else None

            @property
            def c(self):
                return self.u * self.y - self.x * self.v

            def plot_x(self, x):
                y = (self.c - self.a * x) / self.b
                return y

            def plot_y(self, y):
                x = (self.c - self.b * y) / self.a
                return x

            @classmethod
            def det(cls, l0, l1):
                return l0.a * l1.b - l1.a * l0.b

            @classmethod
            def compare_lines(cls, l0, l1, x):
                # Plot the two segments
                y0 = l0.plot_x(x)
                y1 = l1.plot_x(x)
                # If the segments do not match, use the y as a guide
                if abs(abs(y0) - abs(y1)) < finder.leeway:
                    pass
                elif y0 < y1:
                    return -1
                elif y0 > y1:
                    return 1
                # If the segments do match, use the slope (determinant) as a guide
                det = LinearSegment.det(l0, l1)
                # If the determinant is 0, the lines coincide
                if det == 0:
                    return 0
                # If the determinant != 0, one or the other must lie above or below
                elif det > 0:
                    return -1
                elif det < 0:
                    return 1

            @classmethod
            def check_intersection(cls, l0, l1, allow_oob_results=False):
                # Calculate the determinant
                det = LinearSegment.det(l0, l1)
                # If the determinant is 0, the lines have the same slope.
                if det == 0:
                    # If the C components match and the determinants match, the segments are co-linear.
                    if l0.c == l1.c:
                        # If the following conditions are met, there is a line overlap, not a point overlap.
                        # Raise an exception.
                        if (
                            # l0 is a line
                            (l0.t == 'l') or
                            # l1 is a line
                            (l1.t == 'l') or
                            # The left sides extend to infinity
                            (l0.min_x is None and l1.min_x is None) or
                            # The right sides extend to infinity
                            (l0.max_x is None and l1.max_x is None) or
                            # l0 is a l-ray, l1 is a segment
                            (l0.min_x is None and l0.max_x is not None and
                             l1.min_x is not None and l1.max_x is not None and
                             l1.min_x <= l0.max_x <= l1.max_x) or
                            # l1 is a l-ray, l0 is a segment
                            (l1.min_x is None and l1.max_x is not None and
                             l0.min_x is not None and l0.max_x is not None and
                             l0.min_x <= l1.max_x <= l0.max_x) or
                            # l0 is a r-ray, l1 is a segment
                            (l0.min_x is not None and l0.max_x is None and
                             l1.min_x is not None and l1.max_x is not None and
                             l1.min_x <= l0.min_x <= l1.max_x) or
                            # l1 is a r-ray, l0 is a segment
                            (l1.min_x is not None and l1.max_x is None and
                             l0.min_x is not None and l0.max_x is not None and
                             l0.min_x <= l1.min_x <= l0.max_x)
                        ):
                            raise Exception("You have generated a line overlap.")
                        # If the following conditions are met, both lines are segments.
                        elif l0.min_x is not None and l0.max_x is not None and \
                                l1.min_x is not None and l1.max_x is not None:
                            match = sorted([((l0.x, l0.y), (l0.u, l0.v), (l1.x, l1.y), (l1.u, l1.v))])[1:3]
                            if match[0] != match[1]:
                                # print("l1 and l2 match along {}.".format(match))
                                return [(l0, l1, tuple(match))]
                            else:
                                # print("l1 and l2 coincide at point {}.".format(match[1]))
                                return [(l0, l1, tuple(match[:1]))]
                    # If the above conditions are unmet, the parallel or co-linear segments do not coincide
                    else:
                        return []
                # Find the prospective x of the hit
                x_hit = (l0.b * l1.c - l1.b * l0.c) / (l0.b * l1.a - l1.b * l0.a)
                # Find the prospective y of the hit
                y_hit = (l0.a * l1.c - l1.a * l0.c) / (l0.a * l1.b - l1.a * l0.b)
                # Confirm the the x_hit is within bounds
                # print('Hit at ({}, {})'.format(x_hit, y_hit))
                if allow_oob_results:
                    return [(l1, l2, ((x_hit, y_hit),))]
                if not (min([p0[0], p1[0]]) <= x_hit <= max([p0[0], p1[0]])
                        and min([p2[0], p3[0]]) <= x_hit <= max([p2[0], p3[0]])
                        and min([p0[1], p1[1]]) <= y_hit <= max([p0[1], p1[1]])
                        and min([p2[1], p3[1]]) <= y_hit <= max([p2[1], p3[1]])):
                    # print("Intersection point is OOB.")
                    return []
                return [(l1, l2, ((x_hit, y_hit),))]

        class HalfCircle:
            def __init__(self, x, y, r, h):
                if h not in 'tb':
                    raise Exception("You tried to create a LinearSegment with an improper type designation.")
                self.x, self.y, self.r, self.h = x, y, r, h

            def draw(self, wh, min_d, max_d):
                set_stroke_color(0, 0, 1)
                draw_circle((self.x - min_d) * wh / (max_d - min_d),
                            (self.y - min_d) * wh / (max_d - min_d),
                            self.r * wh / (max_d - min_d))

        self.LinearSegment = LinearSegment
        self.HalfCircle = HalfCircle

        self.s_list = [self.LinearSegment(x, y, u, v, 's') for x, y, u, v in s_list]
        self.r_list = [self.LinearSegment(x, y, u, v, 'r') for x, y, u, v in r_list]
        self.l_list = [self.LinearSegment(x, y, u, v, 'l') for x, y, u, v in l_list]
        self.c_list = [self.HalfCircle(x, y, r, 't') for x, y, r in c_list] + \
                      [self.HalfCircle(x, y, r, 'b') for x, y, r in c_list]

    def draw(self, wh):
        # Get bounds
        x_list = [s.x for s in self.s_list + self.r_list + self.l_list] + \
                 [c.x - c.r for c in self.c_list] + \
                 [s.u for s in self.s_list + self.r_list + self.l_list] + \
                 [c.x + c.r for c in self.c_list]
        y_list = [s.y for s in self.s_list + self.r_list + self.l_list] + \
                 [c.y - c.r for c in self.c_list] + \
                 [s.v for s in self.s_list + self.r_list + self.l_list] + \
                 [c.y + c.r for c in self.c_list]
        min_x = min(x_list) - 5
        max_x = max(x_list) + 5
        min_y = min(y_list) - 5
        max_y = max(y_list) + 5
        min_d = min([min_x, min_y])
        max_d = max([max_x, max_y])

        self_ref = self

        def draw():
            clear()
            # Draw in grid
            set_stroke_color(0.1, 0.1, 0.1)
            set_stroke_width(1)
            for n in range(max_d - min_d):
                if (n + min_d) % 5 == 0:
                    n = n * wh / (max_d - min_d)
                    a, b, c, d = 0, n, wh, n
                    draw_line(a, b, c, d)
                    a, b, c, d = n, 0, n, wh
                    draw_line(a, b, c, d)
            # Draw in lines
            set_stroke_color(0, 0, 0)
            set_stroke_width(3)
            for s in self_ref.s_list + self_ref.r_list + self_ref.l_list:
                s.draw(wh, min_d, max_d)
            for c in self_ref.c_list:
                c.draw(wh, min_d, max_d)

        # Start graphics
        start_graphics(draw, width=wh, height=wh)


def find_intersections(s_list, r_list, l_list, c_list):
    """
    Given some Segments, Rays, Lines, and Circles, determine where they all intersect.
    """
    pass


if __name__ == "__main__":
    from random import randint

    s_list = r_list = l_list = c_list = []
    test = "actual"
    # Generate segments
    if test == 'actual':
        s_list = [
            (6, 18, 49, 39),
            (80, 29, 67, 34),
            (90, 76, 10, 4),
        ]
        r_list = [
            (91, 39, 69, -1),
            (53, 57, 8, -36),
            (37, 19, 85, -67),
        ]
        l_list = [
            (56, 30, 106, 25),
            (24, 23, 65, -33),
            (40, 9, 66, 55),
        ]
        c_list = [
            (22, 58, 12),
            (13, 11, 7),
            (1, 23, 1),
        ]
    elif test == 'random':
        s_list = generate_line_segments(8, 10)
    elif test == 't1':
        s_list = [((5, 1), (8, 1)), ((3, 9), (4, 4)), ((2, 9), (6, 2))]
    elif test == 't1':
        s_list = [((1, 6), (5, 3)), ((3, 4), (5, 7)), ((5, 1), (10, 3))][:3]
    elif test == 't1':
        s_list = [((10, 1), (10, 3)), ((0, 4), (6, 3)), ((1, 7), (1, 8))]
    elif test == 't1':
        s_list = [((0, 4), (1, 3)), ((1, 3), (10, 1)), ((7, 1), (8, 2))]
    elif test == 't1':
        s_list = [((1, 4), (4, 9)), ((2, 8), (8, 7)), ((0, 6), (10, 10))]
    elif test == 't1':
        s_list = [((1, 1), (7, 2)), ((3, 1), (6, 2)), ((5, 5), (8, 3))]
    elif test == 't1':
        s_list = [((0, 2), (4, 10)), ((1, 4), (10, 10)), ((2, 6), (7, 2))]
    elif test == 't1':
        s_list = [((3, 10), (9, 7)), ((4, 0), (10, 6)), ((3, 6), (10, 5)), ((9, 0), (9, 3)), ((7, 9), (9, 10)),
                  ((8, 0), (8, 7)), ((8, 10), (10, 2)), ((3, 10), (7, 8))]
    elif test == 't1':
        s_list = [((3, 4), (8, 4)), ((0, 7), (6, 7)), ((1, 4), (8, 10)), ((2, 7), (8, 0)), ((2, 5), (10, 9)),
                  ((1, 8), (10, 7)), ((1, 8), (5, 7))]
    else:
        raise Exception('Invalid test designation')
    print(s_list)
    print()
    # Compare various implementations of the intersection solving problem
    method_counts = {}
    methods = [
        ("Brute", brute_solve),
        # ("Sweep", sweepline_solve),
    ]
    print("Testing Brute.")
    brute_res = brute_solve(s_list, r_list, l_list, c_list)
    print("Total intersections:", len(brute_res))
    print("Testing Efficient.")
    finder = IntersectionFinder(s_list, r_list, l_list, c_list)
    finder.draw(700)
