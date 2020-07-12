from random import randint


LEEWAY = 0.000001


def generate_line_segments(segment_count, bound):
    return list((lambda f: {tuple(sorted([(f(), f()), (f(), f())])) for i in range(segment_count)})(lambda: randint(0, bound)))


# If not parallel, find the x of the hit
def std_form(a, b):
    A = b[1] - a[1]
    B = a[0] - b[0]
    C = A*a[0] + B*a[1]
    return A, B, C


def std_form_seg(seg):
    return std_form(seg[0], seg[1])


def plot(a, b, x):
    A, B, C = std_form(a, b)
    y = (C - A * x) / B
    return y


def cmp_std_forms_at_x(f0, f1, x):
    A0, B0, C0 = f0
    A1, B1, C1 = f1
    # Plot the two segments
    y0 = (C0 - A0 * x) / B0
    y1 = (C1 - A1 * x) / B1
    # If the segments do not match, use the y as a guide
    if abs(abs(y0) - abs(y1)) < LEEWAY:
        pass
    elif y0 < y1:
        return -1
    elif y0 > y1:
        return 1
    # If the segments do match, use the slope (determinant) as a guide
    det = A0 * B1 - A1 * B0
    # If the determinant is 0, the lines coincide
    if det == 0:
        return 0
    # If the determinant != 0, one or the other must lie above or below
    elif det > 0:
        return -1
    elif det < 0:
        return 1


def cmp_segments_at_x(s0, s1, x):
    return cmp_std_forms_at_x(std_form_seg(s0), std_form_seg(s1), x)


def check_intersection(l1, l2, allow_oob_results=False):
    # print("Checking", l1, l2)
    p0, p1 = l1
    p2, p3 = l2

    # Get the standard form for each line
    l1_A, l1_B, l1_C = std_form(p0, p1)
    l2_A, l2_B, l2_C = std_form(p2, p3)
    # Calculate the determinant
    det = (l2_A * l1_B - l1_A * l2_B)
    if det == 0:
        if l1_C != l2_C:
            # print("l1 and l2 are parallel, but not coincident.")
            return []
        elif not (min([p0[0], p1[0]]) <= p2[0] <= max([p0[0], p1[0]]) or
                  min([p0[0], p1[0]]) <= p3[0] <= max([p0[0], p1[0]])):
            # print("l1 and l2 are segments of the same line, but do not overlap.")
            return []
        else:
            match = sorted([p0, p1, p2, p3])[1:3]
            if match[0] != match[1]:
                # print("l1 and l2 match along {}.".format(match))
                return [(l1, l2, tuple(match))]
            else:
                # print("l1 and l2 coincide at point {}.".format(match[1]))
                return [(l1, l2, tuple(match[:1]))]
    # Find the prospective x of the hit
    x_hit = (l1_B * l2_C - l2_B * l1_C) / det
    # Find the prospective y of the hit
    y_hit = (l2_A * l1_C - l1_A * l2_C) / det
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
