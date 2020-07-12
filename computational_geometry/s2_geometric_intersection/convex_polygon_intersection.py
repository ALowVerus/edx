from computational_geometry.s2_geometric_intersection.line_helper_functions import check_intersection, LEEWAY, plot
from computational_geometry.s1_convex_hull.hull_methods_2d import quickhull
import numpy


# Given that the hulls are sorted to a monotone chain, you can find the min & max locations in log(n) time.
def get_hull_min_max_indicies_in_log_time(hull):
    # Define a function to check the polarity if any given point on the hull
    def check_polarity(i):
        p0, p1, p2 = hull[(i-1) % len(hull)], hull[i % len(hull)], hull[(i+1) % len(hull)]
        if p1 > p0 and p1 > p2:
            return '+0'
        elif p0 < p1 < p2:
            return '+'
        elif p0 > p1 > p2:
            return '-'
        elif p1 < p0 and p1 < p2:
            return '-0'
        else:
            raise Exception("Failure! You've reached an impossible state in your search for min/max indices.")

    # Initialize pointers such that all points lie between them
    a, b = 0, len(hull) - 1
    done_splitting_into_halves = False
    while not done_splitting_into_halves:
        # Get the polarity of the two endpoints
        a_polarity = check_polarity(a)
        b_polarity = check_polarity(b)
        # If the polarities mismatch, we have won!
        if ('+' in a_polarity and '-' in b_polarity) or ('-' in a_polarity and '+' in b_polarity):
            done_splitting_into_halves = True
        # If the pointers have diverged to different halves, we have won!
        elif a == b - 1:
            done_splitting_into_halves = True
        # If the pointers have yet to diverge, move towards the light!
        else:
            # Find a point that is halfway between the two pointers
            c = (a + b) // 2
            c_polarity = check_polarity(c)
            # If the polarity of the new point mismatches, we have won!
            if ('+' in a_polarity and '-' in c_polarity) or ('-' in a_polarity and '+' in c_polarity):
                b = c
            # If the polarity still matches,
            else:
                if '+' in c_polarity and hull[c] > hull[a]:
                    a = c
                elif '+' in c_polarity and hull[c] < hull[b]:
                    b = c
                elif '-' in c_polarity and hull[c] < hull[b]:
                    a = c
                elif '-' in c_polarity and hull[c] > hull[a]:
                    b = c
                else:
                    print("Hull cannot be split into two half-hulls.")
                    print(hull)
                    raise Exception("You've failed!", hull[a], hull[b], hull[c], len(hull))

    # Appropriately set the indices for the two sides, one containing the min, one the max
    min_i_lower_bound, min_i_upper_bound = (a, b) if '-' in check_polarity(a) else (b, a)
    max_i_lower_bound, max_i_upper_bound = (a, b) if '+' in check_polarity(a) else (b, a)
    # Account for swaps in direction
    min_i_upper_bound += 0 if min_i_lower_bound < min_i_upper_bound else len(hull)
    max_i_upper_bound += 0 if max_i_lower_bound < max_i_upper_bound else len(hull)
    # Find the minimum
    while min_i_lower_bound != min_i_upper_bound - 1:
        min_i_median_choice = (min_i_lower_bound + min_i_upper_bound) // 2
        median_polarity = check_polarity(min_i_median_choice)
        if '0' in median_polarity:
            min_i_lower_bound = min_i_median_choice
            min_i_upper_bound = min_i_median_choice + 1
        elif '+' in median_polarity:
            min_i_upper_bound = min_i_median_choice
        elif '-' in median_polarity:
            min_i_lower_bound = min_i_median_choice
        else:
            raise Exception("Failure! You've reached an impossible state in your search for min/max indices.")
    min_i = min_i_lower_bound % len(hull)
    # Find the maximum
    while max_i_lower_bound != max_i_upper_bound - 1:
        max_i_median_choice = (max_i_lower_bound + max_i_upper_bound) // 2
        median_polarity = check_polarity(max_i_median_choice)
        if '0' in median_polarity:
            max_i_lower_bound = max_i_median_choice
            max_i_upper_bound = max_i_median_choice + 1
        elif '+' in median_polarity:
            max_i_lower_bound = max_i_median_choice
        elif '-' in median_polarity:
            max_i_upper_bound = max_i_median_choice
        else:
            raise Exception("Failure! You've reached an impossible state in your search for min/max indices.")
    max_i = max_i_lower_bound % len(hull)
    # Return values
    return min_i, max_i


def check_whether_two_convex_polygons_intersect_linear(hull_a, hull_b):
    min_a_i, _ = get_hull_min_max_indicies_in_log_time(hull_a)
    a_left_i = min_a_i - 1
    a_right_i = min_a_i + 1
    min_b_i, _ = get_hull_min_max_indicies_in_log_time(hull_b)
    b_left_i = min_b_i - 1
    b_right_i = min_b_i + 1
    while a_right_i != a_left_i and b_left_i != b_right_i:
        # Get the four current segments
        a_seg_l = hull_a[(a_left_i+1) % len(hull_a)], hull_a[a_left_i]
        b_seg_l = hull_b[(b_left_i+1) % len(hull_b)], hull_b[b_left_i]
        a_seg_r = hull_a[(a_right_i-1) % len(hull_a)], hull_a[a_right_i]
        b_seg_r = hull_b[(b_right_i-1) % len(hull_b)], hull_b[b_right_i]
        # Check for intersections between the four pointers
        segs = [a_seg_l, a_seg_r, b_seg_l, b_seg_r]
        for i0, i1 in [(0, 2), (0, 3), (1, 2), (1, 3)]:
            if len(check_intersection(segs[i0], segs[i1])) > 0:
                return check_intersection(segs[i0], segs[i1])
        # If none of the pairs generated an intersection, sweep onwards
        min_index = segs.index(min(segs, key=lambda t: t[1]))
        if min_index == 0:
            a_left_i -= 1
            a_left_i %= len(hull_a)
        elif min_index == 1:
            a_right_i += 1
            a_right_i %= len(hull_a)
        elif min_index == 2:
            b_left_i -= 1
            b_left_i %= len(hull_b)
        elif min_index == 3:
            b_right_i += 1
            b_right_i %= len(hull_b)
        else:
            raise Exception("How did you not find the minimum of a closed set?")
    # If none of the above actions generated an intersection, you've reached the end.
    return []


# I've got the min and max location generation down to logn, but the intersection detection is iffy.
def check_whether_two_convex_polygons_intersect_log(hull_a, hull_b):
    print("Getting the convex polygon intersections in log time.")
    # Organize the hulls into a dict to prevent redundant code
    extreme_indices = {'a': hull_a, 'b': hull_b}
    # Parse out functions that grab out segments from the inner and outer half-hulls
    half_hull_funcs = {}
    for hull_letter in extreme_indices:
        hull = extreme_indices[hull_letter]
        min_i, max_i, = get_hull_min_max_indicies_in_log_time(hull)
        inner_side_size = max_i - min_i
        outer_side_size = len(hull) - inner_side_size
        if min_i < max_i:
            l_hull_size, r_hull_size = inner_side_size, outer_side_size
        elif min_i > max_i:
            r_hull_size, l_hull_size = inner_side_size, outer_side_size
        else:
            raise Exception("The min and max locations of hull A coincide. Something is wrong.")
        get_left_segment = lambda i: (hull[(min_i + i) % len(hull)], hull[(min_i + i + 1) % len(hull)])
        # print("Checking the get_left_segment function.")
        # for i in range(l_hull_size):
        #     print('Blah', i, get_left_segment(i), hull[(i+min_i) % len(hull)], hull[(i+min_i) % len(hull)] == get_left_segment(i)[0])
        get_right_segment = lambda i: (hull[(min_i - i) % len(hull)], hull[(min_i - i - 1) % len(hull)])
        # print("Checking the get_right_segment function.")
        # for i in range(r_hull_size):
        #     print('Blah', i, get_right_segment(i), hull[(min_i - i) % len(hull)], hull[(min_i - i) % len(hull)] == get_right_segment(i)[0])
        half_hull_funcs[hull_letter] = {"left": {"f": get_left_segment, "l": l_hull_size},
                                        "right": {"f": get_right_segment, "l": r_hull_size}}
    print("Half functions have been generated.")
    # Check the left / right and right / left pairs for intersections
    lr_pairs = [[half_hull_funcs["a"]["left"], half_hull_funcs["b"]["right"]],
                [half_hull_funcs["b"]["left"], half_hull_funcs["a"]["right"]]]
    print()
    for pair_i, (left_hull, right_hull) in enumerate(lr_pairs):
        print('Dealing with pair {}'.format(pair_i))
        li_min, li_max, ri_min, ri_max = 0, left_hull["l"], 0, right_hull["l"]
        lf, rf = left_hull['f'], right_hull['f']
        print('Left side:')
        for li in range(li_max):
            print(lf(li))
        print('Right side:')
        for ri in range(ri_max):
            print(rf(ri))
        done = False
        intersected = False
        while not done and not intersected:
            li_mid, ri_mid = (li_min + li_max) // 2, (ri_min + ri_max) // 2
            l_seg, r_seg = lf(li_mid), rf(ri_mid)
            (l0, l1), (r0, r1) = l_seg, r_seg
            print("L bounds:", li_min, li_max, l_seg)
            print("R bounds:", ri_min, ri_max, r_seg)
            intersection_list = check_intersection(l_seg, r_seg, allow_oob_results=True)
            print(l_seg, r_seg, intersection_list)
            if len(intersection_list) == 0:
                raise Exception("You've reached a null intersection. The lines are parallel.")
            elif len(intersection_list[0][2]) == 1:
                # In this case, there is a single point of intersection.
                x_hit, y_hit = intersection_list[0][2][0]
                # Grab the left relation.
                if y_hit - LEEWAY < plot(l0, l1, x_hit) < y_hit + LEEWAY:
                    l_relation = 0
                elif y_hit - LEEWAY > plot(l0, l1, x_hit):
                    l_relation = -1
                elif y_hit + LEEWAY < plot(l0, l1, x_hit):
                    l_relation = 1
                # Grab the right relation.
                if y_hit - LEEWAY < plot(r0, r1, x_hit) < y_hit + LEEWAY:
                    r_relation = 0
                elif y_hit - LEEWAY > plot(r0, r1, x_hit):
                    r_relation = -1
                elif y_hit + LEEWAY < plot(r0, r1, x_hit):
                    r_relation = 1
                # Depending upon the relations, act accordingly.
                if l_relation == 0 and r_relation == 0:
                    intersected = True
                elif l_relation == 0 and r_relation == 1:
                    pass
                elif l_relation == 0 and r_relation == -1:
                    pass
                elif l_relation == 1 and r_relation == 1:
                    pass
                elif l_relation == 1 and r_relation == -1:
                    pass
                elif l_relation == -1 and r_relation == 1:
                    pass
                elif l_relation == -1 and r_relation == -1:
                    pass
                if li_min == li_max - 1 and ri_min == ri_max - 1:
                    done = True
            elif len(intersection_list[0][2]) == 2:
                raise Exception("The segments {} and {} coincide.".format(l_seg, r_seg))
            else:
                raise Exception("Unknown intersection state.")
            exit()
        if intersected:
            return True
        print()
    print("Congratulations! You've won!")
    return False


def normally_distribute_around_bounded_circle(n, x_min, x_max, y_min, y_max):
    radius = numpy.random.uniform(0.0, 1.0, (n, 1))
    theta = numpy.random.uniform(0., 1., (n, 1)) * pi
    phi = numpy.arccos(1 - 2 * numpy.random.uniform(0.0, 1., (n, 1)))
    x = radius * numpy.sin(theta) * numpy.cos(phi)
    y = radius * numpy.sin(theta) * numpy.sin(phi)
    z = radius * numpy.cos(theta)
    # Generate point objects
    points = [(x[i][0], y[i][0]) for i in range(len(x))]
    # Convert points to points in the unit circle
    points = [((x + 1) / 2, (y + 1) / 2) for x, y in points]
    # Set origin to minimums and scale
    points = [((x * (x_max - x_min)) + x_min, (y * (y_max - y_min)) + y_min) for x, y in points]
    # Scale points up to match drawing size
    points = [(scale_loc(x) // 1, scale_loc(y) // 1) for x, y in points]
    return points


def get_intersection_area_sweepline(hull_a, hull_b):
    """
    This algorithm uses a simple sweepline to generate the intersection of two convex hulls.
    Much of the code is lifted from the linear intersection implementation, as the sweepline is essentially the same.
    """
    # min_a_i, _ = get_hull_min_max_indicies_in_log_time(hull_a)
    # a_left_i = min_a_i - 1
    # a_right_i = min_a_i + 1
    # min_b_i, _ = get_hull_min_max_indicies_in_log_time(hull_b)
    # b_left_i = min_b_i - 1
    # b_right_i = min_b_i + 1
    # while a_right_i != a_left_i and b_left_i != b_right_i:
    #     # Get the four current segments
    #     a_seg_l = hull_a[(a_left_i + 1) % len(hull_a)], hull_a[a_left_i]
    #     b_seg_l = hull_b[(b_left_i + 1) % len(hull_b)], hull_b[b_left_i]
    #     a_seg_r = hull_a[(a_right_i - 1) % len(hull_a)], hull_a[a_right_i]
    #     b_seg_r = hull_b[(b_right_i - 1) % len(hull_b)], hull_b[b_right_i]
    #     # Check for intersections between the four pointers
    #     segs = [a_seg_l, a_seg_r, b_seg_l, b_seg_r]
    #     for i0, i1 in [(0, 2), (0, 3), (1, 2), (1, 3)]:
    #         if len(check_intersection(segs[i0], segs[i1])) > 0:
    #             return check_intersection(segs[i0], segs[i1])
    #     # If none of the pairs generated an intersection, sweep onwards
    #     min_index = segs.index(min(segs, key=lambda t: t[1]))
    #     if min_index == 0:
    #         a_left_i -= 1
    #         a_left_i %= len(hull_a)
    #     elif min_index == 1:
    #         a_right_i += 1
    #         a_right_i %= len(hull_a)
    #     elif min_index == 2:
    #         b_left_i -= 1
    #         b_left_i %= len(hull_b)
    #     elif min_index == 3:
    #         b_right_i += 1
    #         b_right_i %= len(hull_b)
    #     else:
    #         raise Exception("How did you not find the minimum of a closed set?")
    # # If none of the above actions generated an intersection, you've reached the end.
    return []


def get_intersection_area_chasing(hull_a, hull_b):
    """
    This uses O'Rourke's algorithm for edge chasing, rotating around the center until returning to the initial hit.
    """
    print()
    print('Getting the area of the intersection of two hulls.')
    # Find one linear intersection of the two hulls.
    linear_intersection = check_whether_two_convex_polygons_intersect_linear(hull_a, hull_b)
    # If no intersection was found, either there is no intersection, or one encloses the other.
    if len(linear_intersection) == 0:
        # To differentiate, check whether a single point from either hull is inside the other hull.
        return []
    print(linear_intersection[0][0])
    a_segment_hit = linear_intersection[0][0]
    b_segment_hit = linear_intersection[0][1]
    a_index = hull_a.index(a_segment_hit[0])
    b_index = hull_b.index(b_segment_hit[0])
    print(a_index, a_segment_hit, hull_a[a_index], hull_a[(a_index - 1) % len(hull_a)])
    print(b_index, b_segment_hit, hull_b[b_index], hull_b[(b_index - 1) % len(hull_a)])
    print()


# In linearithmic time, get the intersection of a ton of hulls.
def get_intersection_of_many_hulls(hulls):
    def recurse(i0, i1):
        if i0 == i1 - 1:
            return hulls[i0]
        else:
            return get_intersection_area_sweepline(recurse(i0, (i0+i1) // 2), recurse((i0+i1) // 2, i1))
    return recurse(0, len(hulls))


if __name__ == "__main__":
    from random import randint
    from cs1lib import *
    from drawing_lib import *

    points_a = normally_distribute_around_bounded_circle(400, 0, 35, 0, 40)
    points_b = normally_distribute_around_bounded_circle(400, 25, 50, 0, 40)
    # print("A:", points_a)
    # print("B:", points_b)
    hull_a, hull_b = quickhull(points_a), quickhull(points_b)
    print("Hull A:", hull_a)
    print("Hull B:", hull_b)
    hull_a = [(36.0, 139.0), (38.0, 166.0), (43.0, 192.0), (71.0, 231.0), (128.0, 242.0), (137.0, 239.0), (179.0, 220.0),
        (217.0, 155.0), (171.0, 139.0), (139.0, 136.0), (125.0, 135.0), (114.0, 135.0)]
    hull_b = [(183.0, 193.0), (197.0, 211.0), (216.0, 230.0), (241.0, 248.0), (252.0, 239.0), (280.0, 215.0), (300.0, 171.0),
        (280.0, 142.0), (240.0, 135.0), (233.0, 135.0), (221.0, 136.0), (193.0, 146.0), (184.0, 162.0)]

    linear_intersection = check_whether_two_convex_polygons_intersect_linear(hull_a, hull_b)
    print("Via the linear algo, is there an intersection? {}".format(linear_intersection))
    # print("Via the log algo, is there an intersection? {}".format(check_whether_two_convex_polygons_intersect_log(hull_a, hull_b)))

    intersection_area_vertices_chasing = get_intersection_area_chasing(hull_b, hull_a)
    intersection_area_vertices_sweepline = get_intersection_area_sweepline(hull_b, hull_a)

    # Generate two monotone half-hulls for each hull
    a_min_i, a_max_i = get_hull_min_max_indicies_in_log_time(hull_a)
    b_min_i, b_max_i = get_hull_min_max_indicies_in_log_time(hull_b)

    # Draw graphics to understand the workings of the program.
    def draw():
        set_stroke_width(3)
        clear()
        set_fill_color(0, 1, 0)
        set_stroke_color(0, 1, 0)
        for i in range(len(hull_a)):
            (y0, x0), (y1, x1) = hull_a[i], hull_a[(i + 1) % len(hull_a)]
            draw_line(x0, y0, x1, y1)
        # for y, x in points_a:
        #     draw_point(x, y)
        set_fill_color(1, 0, 0)
        set_stroke_color(1, 0, 0)
        for i in range(len(hull_b)):
            (y0, x0), (y1, x1) = hull_b[i], hull_b[(i + 1) % len(hull_b)]
            draw_line(x0, y0, x1, y1)
        # for y, x in points_b:
        #     draw_point(x, y)

        set_fill_color(0, 0, 0)
        set_stroke_color(0, 0, 0)
        draw_point(hull_a[a_min_i][1], hull_a[a_min_i][0])
        draw_point(hull_b[b_min_i][1], hull_b[b_min_i][0])
        draw_point(hull_a[a_max_i][1], hull_a[a_max_i][0])
        draw_point(hull_b[b_max_i][1], hull_b[b_max_i][0])


    start_graphics(draw)
