# Uses python3
import sys
from collections import namedtuple

Segment = namedtuple('Segment', 'start end')


def optimal_points(segments):
    max_seg = (max([s.end for s in segments]) * 1) * 2
    segments = sorted(segments, key=lambda s: s.start * max_seg + s.end)
    points = []
    i = 0
    while i < len(segments):
        j = i + 1
        bounded_end = segments[i].end
        while j < len(segments) and segments[j].start <= bounded_end:
            bounded_end = min([bounded_end, segments[j].end])
            j += 1
        points.append(bounded_end)
        i = j
    return points


if __name__ == '__main__':
    input = sys.stdin.read()
    n, *data = map(int, input.split())
    segments = list(map(lambda x: Segment(x[0], x[1]), zip(data[::2], data[1::2])))
    points = optimal_points(segments)
    print(len(points))
    for p in points:
        print(p, end=' ')
