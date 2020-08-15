class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __str__(self):
        return "({}, {})".format(self.x, self.y)


# Given three colinear points p, q, r, the function checks if
# point q lies on line segment 'pr'
def on_segment(p, q, r):
    if ((q.x <= max(p.x, r.x)) and (q.x >= min(p.x, r.x)) and
            (q.y <= max(p.y, r.y)) and (q.y >= min(p.y, r.y))):
        return True
    return False


def orientation(p, q, r):
    val = (float(q.y - p.y) * (r.x - q.x)) - (float(q.x - p.x) * (r.y - q.y))
    if val > 0:
        # Clockwise orientation
        return 1
    elif val < 0:
        # Counterclockwise orientation
        return 2
    else:
        # Colinear orientation
        return 0


# The main function that returns true if
# the line segment 'p1q1' and 'p2q2' intersect.
def do_intersect(p1, q1, p2, q2):
    # Find the 4 orientations required for
    # the general and special cases
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)
    # General case
    if (o1 != o2) and (o3 != o4):
        return True
    # Special Cases
    # p1 , q1 and p2 are colinear and p2 lies on segment p1q1
    if (o1 == 0) and on_segment(p1, p2, q1):
        return True
    # p1 , q1 and q2 are colinear and q2 lies on segment p1q1
    if (o2 == 0) and on_segment(p1, q2, q1):
        return True
    # p2 , q2 and p1 are colinear and p1 lies on segment p2q2
    if (o3 == 0) and on_segment(p2, p1, q2):
        return True
    # p2 , q2 and q1 are colinear and q1 lies on segment p2q2
    if (o4 == 0) and on_segment(p2, q1, q2):
        return True
    # If none of the cases
    return False


# Define a function to get half-hulls in a single direction.
def half_hull(sorted_points):
    hull = []
    for p in sorted_points:
        # It's okay to only check CCW, as this function will be run on both an initial and a reversed list.
        while len(hull) > 1 and orientation(hull[-2], hull[-1], p) != 2:
            hull.pop()
        hull.append(p)
    return hull


if __name__ == "__main__":
    res = []
    case_count = int(input())
    for case_number in range(case_count):
        lines = []
        line_count = int(input())
        for line_number in range(line_count):
            x, y1, y2 = [int(n) for n in input().split(' ')]
            lines.append((x, y1, y2))
        # Sort lines according to x
        lines = sorted(lines, key=lambda l: l[0])
        # Generate a list of upper and lower points
        upper_points = [Point(x, y1) for x, y1, y2 in lines]
        lower_points = [Point(x, y2) for x, y1, y2 in lines]
        # Get the hulls
        upper_hull = half_hull(upper_points)
        lower_hull = half_hull(lower_points[::-1])[::-1]
        # Confirm that there is no overlap of the lines
        upper_i = 0
        lower_i = 0
        hit_cross = False
        while not hit_cross and upper_i < len(upper_hull) - 1 and lower_i < len(lower_hull) - 1:
            u1, u2 = upper_hull[upper_i + 0], upper_hull[upper_i + 1]
            l1, l2 = lower_hull[lower_i + 0], lower_hull[lower_i + 1]
            # Check whether the currently selected segments cross
            hit_cross = do_intersect(u1, u2, l1, l2)
            # Move the pointers forward to check further segments
            if u2.x < l2.x:
                upper_i += 1
            elif u2.x > l2.x:
                lower_i += 1
            else:
                upper_i += 1
                lower_i += 1
        # Record the result
        res.append(hit_cross)
    # Print the output
    print(''.join(['Y' if not hit_cross else 'N' for hit_cross in res]))
