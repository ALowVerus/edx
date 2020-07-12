#Uses python3
from math import sqrt
import sys


def cmp(a, b):
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2


def dist(a, b):
    return sqrt(cmp(a, b))


def closest_pair(root_points):
    seen = set()
    for point in root_points:
        if point in seen:
            return (point, point)
        seen.add(point)
    del seen

    points = sorted(root_points, key=lambda p: p[0])

    meta = {}

    def update_best(a, b):
        meta["best"] = (a, b)
        meta["best_cmp"] = cmp(a, b)
        meta["best_dist"] = dist(a, b)

    update_best(root_points[0], root_points[1])

    def brute_force(i_o, i_f, indent):
        for i in range(i_o, i_f - 1):
            sp = points[i]
            for j in range(i + 1, i_f):
                fp = points[j]
                if meta["best_cmp"] > cmp(sp, fp):
                    update_best(sp, fp)

    def recurse(i_o, i_f, indent):
        # If few points, brute force it
        if i_f - i_o <= 3:
            brute_force(i_o, i_f, indent)
        # Else, recurse
        else:
            i_m = (i_o + i_f) // 2
            recurse(i_o, i_m, indent + 1)
            recurse(i_m, i_f, indent + 1)
            # Check within bounds
            i_a, i_b = i_m, i_m + 1
            while i_a > i_o and points[i_m][0] - points[i_a][0] < meta["best_dist"]:
                i_a -= 1
            while i_b < i_f and points[i_b][0] - points[i_m][0] < meta["best_dist"]:
                i_b += 1
            strip_a = sorted(points[i_a:i_m], key=lambda p: p[1])
            strip_b = sorted(points[i_m:i_b], key=lambda p: p[1])
            k_a, k_b = 0, 0
            while k_a < len(strip_a) and k_b < len(strip_b):
                if strip_a[k_a][1] < strip_b[k_b][1]:
                    root = strip_a[k_a]
                    branch_strip = strip_b
                    branch_i = k_b
                else:
                    root = strip_b[k_b]
                    branch_strip = strip_a
                    branch_i = k_a
                while branch_i < len(branch_strip) and branch_strip[branch_i][1] - root[1] < meta["best_dist"]:
                    if dist(branch_strip[branch_i], root) < meta["best_dist"]:
                        update_best(branch_strip[branch_i], root)
                    branch_i += 1
                if strip_a[k_a][1] < strip_b[k_b][1]:
                    k_a += 1
                else:
                    k_b += 1

    recurse(0, len(points), 0)
    return meta['best']


if __name__ == '__main__':
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n = data[0]
    x = data[1::2]
    y = data[2::2]
    best_pair = closest_pair([(a, b) for a, b in zip(x, y)])
    print("{0:.9f}".format(dist(best_pair[0], best_pair[1])))
