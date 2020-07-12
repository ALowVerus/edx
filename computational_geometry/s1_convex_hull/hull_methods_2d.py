import math


# Check for left turns in constant time
def is_ccw_turn(p0, p1, p2):
    return (p1[0] - p0[0]) * (p2[1] - p0[1]) - (p2[0] - p0[0]) * (p1[1] - p0[1]) > 0


def triangle_area(a, b, c):
    return abs(a[0] * (b[1] - c[1]) + b[0] * (c[1] - a[1]) + c[0] * (a[1] - b[1])) / 2


def quickhull(points):
    """
    Iteratively generate a hull by finding items with the maximum distance from the current hull, adding them, and repeating.
    Currently very inefficient.
    """
    def dist(a, b, c):
        A = b[1] - a[1]
        B = a[0] - b[0]
        C = a[1] * b[0] - a[0] * b[1]
        return abs(A * c[0] + B * c[1] + C)

    def quickhull_recurse(a, b, targets, indent=1):
        # Remove colinear points
        targets = [p for p in targets if dist(a, b, p) != 0]
        # If no targets exist, be done
        if len(targets) == 0:
            return []
        max_dist = max([dist(a, b, p) for p in targets])
        m = min([p for p in targets if dist(a, b, p) == max_dist])
        l_targets = quickhull_recurse(a, m, [p for p in targets if not is_ccw_turn(m, a, p)], indent + 1)
        r_targets = quickhull_recurse(m, b, [p for p in targets if not is_ccw_turn(b, m, p)], indent + 1)
        return l_targets + [m] + r_targets

    # Grab two extreme points
    least, most = min(points), max(points)
    # Split into those points above and below
    points = [p for p in points if p != most and p != least]
    top = quickhull_recurse(least, most, [p for p in points if is_ccw_turn(least, most, p)])
    bot = quickhull_recurse(most, least, [p for p in points if not is_ccw_turn(least, most, p)])
    # Generate the final result
    return [least] + top + [most] + bot


def unsorted_merge_hull(points):
    """
    Generate a merged hull by splitting the hull arbitrarily, generating two parting hulls, and reconciling.
    First, remove all points in hull 2's inner edge, if the centroid of hull 1 is outside hull 2.
    Then, reconcile all points into a single queue, ordered by angle, then distance.
    Finally, run a graham scan on this new monotone ring.
    DOESN'T CURRENTLY RUN TOO WELL.
    """
    # If the number of points is small enough, crank out a solution.
    if len(points) <= 5:
        return double_half_hull(points)
    # If the number of points is high, divide and conquer.
    else:
        # Generate partial hulls
        a, b = unsorted_merge_hull(points[:len(points) // 2]), unsorted_merge_hull(points[len(points) // 2:])
        # Find a point inside the first partial hull
        c = (sum([x for x, y in a[:3]]) / 3, sum([y for x, y in a[:3]]) / 3)
        # Determine the targent line points of the second partial hull to the centroid, if applicable
        i = 0
        while i < len(b) or is_ccw_turn(c, b[i], b[(i + 1) % len(b)]) or is_ccw_turn(c, b[i], b[(i - 1) % len(b)]):
            i += 1
        # If one tangent is found, find the other
        if i < len(b):
            j = 0
            while j < len(b) or is_ccw_turn(c, b[j], b[(j + 1) % len(b)]) or is_ccw_turn(c, b[j], b[(j - 1) % len(b)]):
                j += 1
            # Kill the points between the tangents
            if i < j:
                b = b[i:j]
            else:
                b = b[j:] + b[:i]
        # Merge to partial hulls into a single queue
        q = []
        i_a, i_b = 0, 0
        while i_a < len(a) or i_b < len(b):
            pass
        if i_a < len(a): q.extend(a[i_a:])
        if i_b < len(b): q.extend(b[i_b:])
        # Run a graham scan on the queue
        # Return a valid hull


def x_laced_merge_hull(points):
    """
    Generate a merged hull by splitting the hull along a single axis, generating a series of partial hulls, and merging.
    The main benefit of this is the ability to parallel process.
    The checking for colinear points and the determination of the min/max could be optimized:
    - The colinear points only occur at the junction of left and right sections. Only 2 checks are needed, not N.
    - The min/max come from the min and max of either side, so they could be determined in constant time. Fix pointers.
    """
    sorted_points = sorted(points)
    # Remove doubles along the x axis
    x_laced_points = []
    for p in sorted_points:
        x_laced_points.append(p)
        if len(x_laced_points) >= 3 and x_laced_points[-1][0] == x_laced_points[-2][0] == x_laced_points[-3][0]:
            x_laced_points.pop(-2)

    def sew(l_h, r_h, l_o, r_o, direction):
        # Start sewing at the extreme middle of the partial hulls.
        l_i, r_i = l_o, r_o
        found_both = False
        while not found_both:
            # If either the left or right is moved, re-loop.
            found_both = True
            # Shift the right pointer as much as possible toward the extreme
            moving_right = True
            while moving_right:
                if direction == "top":
                    m_res = is_ccw_turn(r_h[(r_i + 1) % len(r_h)], r_h[r_i], l_h[l_i])
                    p_res = is_ccw_turn(r_h[(r_i - 1) % len(r_h)], r_h[r_i], l_h[l_i])
                elif direction == "bot":
                    m_res = is_ccw_turn(l_h[l_i], r_h[r_i], r_h[(r_i + 1) % len(r_h)])
                    p_res = is_ccw_turn(l_h[l_i], r_h[r_i], r_h[(r_i - 1) % len(r_h)])
                if m_res == p_res == False:
                    moving_right = False
                else:
                    r_i = (r_i + (1 if direction == "top" else -1)) % len(r_h)
                    found_both = False
            # Shift the left pointer as much as possible towards the extreme
            moving_left = True
            while moving_left:
                if direction == "top":
                    m_res = is_ccw_turn(r_h[r_i], l_h[l_i], l_h[(l_i + 1) % len(l_h)])
                    p_res = is_ccw_turn(r_h[r_i], l_h[l_i], l_h[(l_i - 1) % len(l_h)])
                elif direction == "bot":
                    m_res = is_ccw_turn(l_h[(l_i + 1) % len(l_h)], l_h[l_i], r_h[r_i])
                    p_res = is_ccw_turn(l_h[(l_i - 1) % len(l_h)], l_h[l_i], r_h[r_i])
                if m_res == p_res == False:
                    moving_left = False
                else:
                    l_i = (l_i + (-1 if direction == "top" else 1)) % len(l_h)
                    found_both = False
        # Return indexes for the left and right nodes that will be bridged to merge the hulls.
        return l_i, r_i

    def x_laced_recurse(l_i=0, r_i=len(x_laced_points)):
        # If there are under 5 points, use an inefficient algo.
        if r_i - l_i <= 5:
            sub_points = x_laced_points[l_i:r_i]
            hull = double_half_hull(sub_points)
            return hull.index(min(hull)), hull.index(max(hull)), hull
        # If there are over 5 points, recurse.
        else:
            # Recurse until there are two half-hulls of equal heft
            l_min_i, l_max_i, l_h = x_laced_recurse(l_i, (l_i + r_i) // 2)
            r_min_i, r_max_i, r_h = x_laced_recurse((l_i + r_i) // 2, r_i)
            # Start with a line from the rightmost left point to the leftmost right point, move until can no longer
            # Move the two lines, one up, one down until they can no longer be rotated to increase their encompassings
            # It is the SEWING function that is screwed up.
            bot_i_l, bot_i_r = sew(l_h, r_h, l_max_i, r_min_i, 'bot')
            top_i_l, top_i_r = sew(l_h, r_h, l_max_i, r_min_i, 'top')
            # Join along the highlighted points, so as to merge the two partial hulls into a single spanning hull
            hull = []
            # Get the left side
            if bot_i_l <= top_i_l:
                hull.extend(l_h[bot_i_l:top_i_l+1])
            elif bot_i_l > top_i_l:
                hull.extend(l_h[bot_i_l:])
                hull.extend(l_h[:top_i_l+1])
            # Get the right side
            if top_i_r <= bot_i_r:
                hull.extend(r_h[top_i_r:bot_i_r+1])
            elif top_i_r > bot_i_r:
                hull.extend(r_h[top_i_r:])
                hull.extend(r_h[:bot_i_r+1])
            # Validate for introduced colinear points. You could get this in O(1), but I'm lazy, and that would be complicated.
            max_index = hull.index(max(hull))
            i = (max_index + 1) % len(hull)
            new_hull = [hull[max_index]]
            while i != max_index:
                new_hull.append(hull[i])
                while len(new_hull) >= 3 and not is_ccw_turn(new_hull[-3], new_hull[-2], new_hull[-1]):
                    new_hull.pop(-2)
                i = (i + 1) % len(hull)
            while len(new_hull) >= 3 and not is_ccw_turn(new_hull[-2], new_hull[-1], new_hull[0]):
                new_hull.pop(-1)
            hull = new_hull
            # Return the result
            return hull.index(min(hull)), hull.index(max(hull)), hull

    return x_laced_recurse()[2]


def graham_scan_hull(points):
    # Get LTL
    m = max([n[1] for n in points])
    o = min(points, key=lambda p: (p[0] * m + p[1]))
    # Sort according to angle from origin
    points = sorted(points, key=lambda p: (p[0] * m + p[1]))
    points = sorted(points[1:], key=lambda p: math.atan2(p[0] - o[0], p[1] - o[1]))
    # Initialize the hull with origin and item with lowest or highest angle
    h, points = [points[-1], o, points[0]], points[1:]
    # Iterate over the points
    for p in points:
        # Append the next point
        h.append(p)
        # Kill 2nd-to-last until reaching a state of convexity
        done = False
        # Pop until not at a ccw turn
        while len(h) > 3 and not is_ccw_turn(h[-1], h[-2], h[-3]):
            h.pop(-2)
    h = [[p[0], p[1]] for p in h[:-1]]
    return (h[2:] + h[:2])[::-1]


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


def hull_method(points):
    # Remove point doubles
    points = [list(p) for p in set([tuple(p) for p in points])]
    # Print the points
    print(points if len(points) < 80 else "{}...".format(points[:80]), '\n')
    # print("unsorted_merge_hull:")
    # res_unsorted_merge_hull = unsorted_merge_hull(points)
    # print(res_unsorted_merge_hull, '\n')
    print("quickhull:")
    res_quickhull = quickhull(points)
    print(res_quickhull, '\n')
    print("x_laced_merge hull:")
    res_x_laced_merge_hull = x_laced_merge_hull(points)
    print(res_x_laced_merge_hull, '\n')
    print("graham_scan_hull:")
    res_graham_scan_hull = graham_scan_hull(points)
    print(res_graham_scan_hull, '\n')
    print("double_half_hull:")
    res_double_half_hull = double_half_hull(points)
    print(res_double_half_hull, '\n')
    hash_checkers = []
    for hull in [res_quickhull, res_x_laced_merge_hull, res_graham_scan_hull, res_double_half_hull]:
        hash_checkers.append({tuple(p) for p in hull})
    fail_to_matches = sum(hash_checkers[i] != hash_checkers[i + 1] for i in range(len(hash_checkers) - 1))
    return [] if fail_to_matches > 0 else res_double_half_hull