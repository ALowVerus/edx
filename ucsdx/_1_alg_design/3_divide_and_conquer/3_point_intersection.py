# Uses python3
import sys


class SegmentNode:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.max_end = end
        self.lesser = None
        self.greater = None

    def insert(self, start, end):
        self.max_end = max([self.max_end, end])
        if start < self.start:
            if self.lesser is None:
                self.lesser = SegmentNode(start, end)
            else:
                self.lesser.insert(start, end)
        else:
            if self.greater is None:
                self.greater = SegmentNode(start, end)
            else:
                self.greater.insert(start, end)

    def query(self, x, res=None, indent=0):
        # print('  ' * indent, x, res, self.start, self.end)
        if res is None:
            res = []
        if x > self.max_end:
            pass
        elif x < self.start:
            if self.lesser is not None:
                self.lesser.query(x, res, indent+1)
        else:
            if x <= self.end:
                res.append((self.start, self.end))
            if self.lesser is not None and self.lesser.max_end >= x:
                self.lesser.query(x, res, indent+1)
            if self.greater is not None:
                self.greater.query(x, res, indent+1)
        return res

    def print_tree(self, indent=0):
        print('{}Seg: ({}, {}), max_end={}'.format('  ' * indent, self.start, self.end, self.max_end))
        if self.lesser is not None:
            self.lesser.print_tree(indent+1)
        if self.greater is not None:
            self.greater.print_tree(indent+1)


def count_segment_hits(starts, ends, points):
    # Generate a tree search structure
    segments = list(zip(starts, ends))
    tree = SegmentNode(segments[0][0], segments[0][1])
    for start, end in segments[1:]:
        tree.insert(start, end)
    # tree.print_tree()
    # Return query results
    res = [tree.query(x) for x in points]
    # print(res)
    res = [len(r) for r in res]
    return res


def process(text):
    data = list(map(int, text.split()))
    n = data[0]
    m = data[1]
    starts = data[2:2 * n + 2:2]
    ends = data[3:2 * n + 2:2]
    points = data[2 * n + 2:]
    print(starts)
    print(ends)
    print(points)
    print(count_segment_hits(starts, ends, points))
    print()


t0 = """
2 3
0 5
7 10
1 6 11
"""

t1 = """
3 2
0 5
-3 2
7 10
1 6
"""

process(t0)
process(t1)


if __name__ == '__main__':
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n = data[0]
    m = data[1]
    starts = data[2:2 * n + 2:2]
    ends = data[3:2 * n + 2:2]
    points = data[2 * n + 2:]
    # use fast_count_segments
    cnt = count_segment_hits(starts, ends, points)
    for x in cnt:
        print(x, end=' ')
