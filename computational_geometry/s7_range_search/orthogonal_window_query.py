from random import shuffle
from cs1lib import *


class SegmentTree:
    """
    This structure will take in a series of horizontal lines where y1 = y2.
    It will arrange them into a search tree.
    It has LogN performance when searching for the counts of matches to the search.
    """
    def __init__(self, segments):
        for s in segments:
            if type(s) is not SegmentTree.SegmentTreeSegment:
                raise Exception("You're trying to propogate non-segment items.")
        self.root = SegmentTree.SegmentTreeYNode([s for s in segments], None)

    def print(self):
        print("Segment Tree:")
        self.root.print(indent=1)

    def draw(self):
        self.root.draw()

    def query(self, x1, x2, y1, y2, verbose=False):
        if x1 > x2 or y1 > y2:
            raise Exception("Your query bounds are invalid.")
        res = {}
        if verbose:
            print('Querying against {}.'.format((x1, x2, y1, y2)))
        self.root.query(x1, x2, y1, y2, None, None, None, None, res, 0, verbose)
        return [v[1] for k, v in res.items()]

    def count_items(self):
        d = {}
        q = [self.root]
        while q:
            item = q.pop()
            if item is not None:
                if id(item.segment) not in d:
                    d[id(item.segment)] = 0
                d[id(item.segment)] += 1
                if type(item) == SegmentTree.SegmentTreeYNode:
                    q.append(item.t)
                    q.append(item.b)
                    q.append(item.c)
                elif type(item) == SegmentTree.SegmentTreeXNode:
                    q.append(item.l)
                    q.append(item.r)
                    q.append(item.cl)
                    q.append(item.cr)
        counts = {}
        for v in [v for k, v in d.items()]:
            if v not in counts:
                counts[v] = 0
            counts[v] += 1
        print(counts)
        return len(d)

    class SegmentBaseNode:
        def __init__(self, segment, side, center_side):
            self.segment, self.side, self.center_side = segment, side, center_side

        def __str__(self):
            return '{}; c_side: {}, side: {}'.format(str(self.segment), self.center_side, self.side)

        def falls_within(self, x1, x2, y1, y2):
            return self.segment.falls_within(x1, x2, y1, y2)

        @property
        def x(self):
            return self.segment.x1 if self.side == 'x1' else self.segment.x2 if self.side == 'x2' else None

        @property
        def y(self):
            return self.segment.y

    class SegmentTreeYNode(SegmentBaseNode):
        def __init__(self, segments, center_side):
            self.count = len(segments)
            segment = SegmentTree.SegmentTreeSegment.grab_y_median(segments)
            super().__init__(segment, None, center_side)
            self.t = self.b = self.c = None
            t_list = [s for s in segments if s.y > self.y]
            b_list = [s for s in segments if s.y < self.y]
            c_list = [s for s in segments if s.y == self.y]
            # print("Now processing {} as a Y-Node.".format(str(self)))
            # print("Above:", [str(s) for s in t_list])
            # print("Below:", [str(s) for s in b_list])
            # print("Inline:", [str(s) for s in c_list])
            # print()
            if t_list:
                self.t = SegmentTree.SegmentTreeXNode(t_list, center_side)
            if b_list:
                self.b = SegmentTree.SegmentTreeXNode(b_list, center_side)
            if c_list:
                self.c = SegmentTree.SegmentTreeXNode(c_list, center_side)

        def query(self, x1, x2, y1, y2, bx1, bx2, by1, by2, res, indent, verbose):
            if verbose: print('{}{}: {}; bounds: {}'.format('\t' * indent, 'Y', str(self), (bx1, bx2, by1, by2)))
            if self.falls_within(x1, x2, y1, y2):
                if id(self.segment) not in res:
                    res[id(self.segment)] = [0, self.segment]
                res[id(self.segment)][0] += 1
            if self.t and self.y < y2:
                if verbose: print('{}{}'.format('\t' * indent, ' T'))
                self.t.query(x1, x2, y1, y2, bx1, bx2, by1, self.y, res, indent + 1, verbose)
            if self.b and self.y > y1:
                if verbose: print('{}{}'.format('\t' * indent, ' B'))
                self.b.query(x1, x2, y1, y2, bx1, bx2, self.y, by2, res, indent + 1, verbose)
            if self.c and y1 <= self.y <= y2:
                if verbose: print('{}{}'.format('\t' * indent, ' C'))
                self.c.query(x1, x2, y1, y2, bx1, bx2, self.y, self.y, res, indent + 1, verbose)

        def print(self, indent):
            print('{}{}: {}'.format('\t' * indent, 'Y', str(self)))
            if self.t:
                print('{}{}'.format('\t' * indent, 'T'))
                self.t.print(indent + 1)
            if self.b:
                print('{}{}'.format('\t' * indent, 'B'))
                self.b.print(indent + 1)
            if self.c:
                print('{}{}'.format('\t' * indent, 'C'))
                self.c.print(indent + 1)

        def draw(self):
            self.segment.draw()
            if self.t: self.t.draw()
            if self.b: self.b.draw()
            if self.c: self.c.draw()

    class SegmentTreeXNode(SegmentBaseNode):
        def __init__(self, segments, center_side):
            self.count = len(segments)
            median, side = SegmentTree.SegmentTreeSegment.grab_x_median(segments, center_side)
            super().__init__(median, side, center_side)
            self.l = self.r = self.cl = self.cr = None
            l_list = [s for s in segments if s.x2 < self.x]
            r_list = [s for s in segments if s.x1 > self.x]
            c_list = [s for s in segments if s.x1 <= self.x <= s.x2]
            # print("Now processing {} as a X-Node.".format(str(self)))
            # print("L:", [str(s) for s in l_list])
            # print("R:", [str(s) for s in r_list])
            # print("C:", [str(s) for s in c_list])
            # print()
            if len(l_list) + len(r_list) + len(c_list) != len(segments):
                raise Exception("You've somehow missed some segment assignments along the X-axis.")
            if l_list:
                self.l = SegmentTree.SegmentTreeYNode(l_list, center_side)
            if r_list:
                self.r = SegmentTree.SegmentTreeYNode(r_list, center_side)
            if c_list:
                if center_side is None or center_side == "x1":
                    self.cl = SegmentTree.SegmentTreeYNode([s for s in c_list], 'x1')
                if center_side is None or center_side == "x2":
                    self.cr = SegmentTree.SegmentTreeYNode([s for s in c_list], 'x2')

        def query(self, x1, x2, y1, y2, bx1, bx2, by1, by2, res, indent, verbose):
            if verbose: print('{}{}: {}; bounds: {}'.format('\t' * indent, 'X', str(self), (bx1, bx2, by1, by2)))
            if self.falls_within(x1, x2, y1, y2):
                if id(self.segment) not in res:
                    res[id(self.segment)] = [0, self.segment]
                res[id(self.segment)][0] += 1
            if self.l and self.x >= x1:
                if verbose: print('{}{}'.format('\t' * indent, ' L'))
                self.l.query(x1, x2, y1, y2, bx1, self.x, by1, by2, res, indent + 1, verbose)
            if self.r and self.x <= x2:
                if verbose: print('{}{}'.format('\t' * indent, ' R'))
                self.r.query(x1, x2, y1, y2, self.x, bx2, by1, by2, res, indent + 1, verbose)
            # Handle the center parts when the current x does not intersect the search space
            if self.cr and self.x < x1 and (bx2 is None or x1 <= bx2 <= x2):
                if verbose: print('{}{}'.format('\t' * indent, ' CR'))
                self.cr.query(x1, x2, y1, y2, bx1, bx2, by1, by2, res, indent + 1, verbose)
            elif self.cl and self.x > x2 and (bx1 is None or x1 <= bx1 <= x2):
                if verbose: print('{}{}'.format('\t' * indent, ' CL'))
                self.cl.query(x1, x2, y1, y2, bx1, bx2, by1, by2, res, indent + 1, verbose)
            # Handle the center parts when the current x is between the x1 and x2 bounds
            else:
                if self.cl and (self.center_side is None or self.center_side == 'x1'):
                    if verbose: print('{}{}'.format('\t' * indent, ' CL'))
                    self.cl.query(x1, x2, y1, y2, bx1, bx2, by1, by2, res, indent + 1, verbose)
                if self.cr and (self.center_side is None or self.center_side == 'x2'):
                    if verbose: print('{}{}'.format('\t' * indent, ' CR'))
                    self.cr.query(x1, x2, y1, y2, bx1, bx2, by1, by2, res, indent + 1, verbose)

        def print(self, indent):
            print('{}{}: {}'.format('\t' * indent, 'X', str(self)))
            if self.l:
                print('{}{}'.format('\t' * indent, 'L'))
                self.l.print(indent + 1)
            if self.r:
                print('{}{}'.format('\t' * indent, 'R'))
                self.r.print(indent + 1)
            if self.cl:
                print('{}{}'.format('\t' * indent, 'CL'))
                self.cl.print(indent + 1)
            if self.cr:
                print('{}{}'.format('\t' * indent, 'CR'))
                self.cr.print(indent + 1)

        def draw(self):
            self.segment.draw()
            if self.l: self.l.draw()
            if self.r: self.r.draw()
            if self.cl: self.cl.draw()

    class SegmentTreeSegment:
        def __init__(self, x1, x2, y):
            if x1 > x2:
                raise Exception("You've tried to create a SegmentTreeSegment with unsorted x's.")
            self.x1, self.x2, self.y = x1, x2, y

        def __str__(self):
            return '({}, {}, {})'.format(self.x1, self.x2, self.y)

        def draw(self):
            draw_line(self.x1, self.x2, self.y, self.y)
            draw_circle(self.x1, self.y, 5)
            draw_circle(self.x1, self.y, 5)

        def falls_within(self, x1, x2, y1, y2):
            return y1 <= self.y <= y2 and self.x1 <= x2 and self.x2 >= x1

        @classmethod
        def grab_x_median(cls, segments, side):
            points = []
            if side is None or side == "x1":
                points.extend([['x2', s] for s in segments])
            if side is None or side == "x2":
                points.extend([['x2', s] for s in segments])
            while len(points) > 1:
                points = [sorted(points[i * 5: i * 5 + 5],
                                 key=lambda s: s[1].x1 if s[0] == 'x1' else s[1].x2 if s[0] == 'x2' else None)
                          for i in range((len(points) - 1) // 5 + 1)]
                points = [g[len(g) // 2] for g in points]
            side, segment = points[0]
            segments.remove(segment)
            return segment, side

        @classmethod
        def grab_y_median(cls, segments):
            segs = [s for s in segments]
            while len(segs) > 1:
                groups = [segs[i * 5: i * 5 + 5] for i in range((len(segs) - 1) // 5 + 1)]
                groups = [sorted(group, key=lambda s: s.y) for group in groups]
                segs = [g[len(g) // 2] for g in groups]
            y_median_segment = segs[0]
            segments.remove(y_median_segment)
            return y_median_segment


if __name__ == "__main__":
    from random import randint
    from time import time
    # coordinate_max, line_count, query_count = 100, 20, 20
    coordinate_max = 1000
    line_count = 60000
    query_count = 100

    coordinates = [(randint(0, coordinate_max), randint(0, coordinate_max), randint(0, coordinate_max))
                   for i in range(line_count)]
    coordinates = [(min([x1, x2]), max([x1, x2]), y) for x1, x2, y in coordinates]
    # print('\t' + '\n\t'.join([', '.join([str(n) for n in tup]) for tup in coordinates]))
    segments = [SegmentTree.SegmentTreeSegment(x1, x2, y) for x1, x2, y in coordinates]
    print("Populating the tree.")
    t0 = time()
    tree = SegmentTree(segments)
    print("Tree populated in {}s.".format(time() - t0))

    queries = [[randint(0 - 5, coordinate_max + 5) for i in range(2)] for query_i in range(query_count)]
    queries = [(x, x + 10, y, y + 10) for x, y in queries]
    queries = list(set(queries))
    segment_sorting_key = lambda s: s.y * 100000000 + s.x1 * 10000 + s.x2
    run_i = 0
    running_average = 0
    verbose = False
    for x1, x2, y1, y2 in queries:
        t0c = time()
        count_c = len(tree.query(x1, x2, y1, y2, verbose))
        tc = time() - t0c + 0.0000000000001
        t0s = time()
        count_s = len([s for s in segments if s.falls_within(x1, x2, y1, y2)])
        ts = time() - t0s + 0.0000000000001
        running_average = (running_average * run_i + tc / ts) / (run_i + 1)
        run_i += 1
        print('Comp: {:6}, t = {:f};'.format(count_c, tc),
              'Simp: {:6}, t = {:f};'.format(count_s, ts),
              'Gains: {:f}'.format(tc / ts),
              'Running average gains: {:f}'.format(running_average),
              '\n\n\n' if verbose else '')
        if count_c != count_s:
            raise Exception()
