# Check for left turns in constant time
def is_ccw_turn(p0, p1, p2):
    return (p1[0] - p0[0]) * (p2[1] - p0[1]) - (p2[0] - p0[0]) * (p1[1] - p0[1]) > 0


# Generate a merged hull by generating two max-size, half-hulls with CW and CCW cardinality, then joining them.
def double_half_hull(points):
    # Sort the points along an axis to make them monotone.
    sorted_points = sorted(points)

    # Define a function to get half-hulls in a single direction.
    def half_hull(sorted_points):
        hull = []
        for p in sorted_points:
            # It's okay to only check CCW, as this function will be run on both an initial and a reversed list.
            while len(hull) > 1 and not is_ccw_turn(hull[-2], hull[-1], p):
                hull.pop()
            hull.append(p)
        hull.pop()
        return hull

    # Call the half-hull function twice - once to get the right side, once the left.
    return half_hull(sorted_points) + half_hull(reversed(sorted_points))


if __name__ == "__main__":
    n = int(input())
    lines = [input() for i in range(n)]
    parts = [line.split(' ') for line in lines]
    points = [(int(part[0]), int(part[1])) for part in parts]
    indices = {points[i]: i for i in range(len(points))}
    hull_items = double_half_hull(points)
    hull_indices = [indices[point] + 1 for point in hull_items]
    res = 1
    for index in hull_indices:
        res *= index
    res *= len(hull_indices)
    res %= len(points) + 1
    print(res)
