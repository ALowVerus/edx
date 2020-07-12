def is_ccw_turn(p0, p1, p2):
    return (p1[0] - p0[0]) * (p2[1] - p0[1]) - (p2[0] - p0[0]) * (p1[1] - p0[1]) > 0


def triangle_area(a, b, c):
    return abs(a[0] * (b[1] - c[1]) + b[0] * (c[1] - a[1]) + c[0] * (a[1] - b[1])) / 2


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


class Palette:
    def __init__(self, paints):
        self.paints = None
        self.hull = double_half_hull(paints)

    def validate(self, point):
        # Using the first point in the hull as a root, use binary search to find that triangle which encloses the point.
        i0, i1 = 1, len(self.hull) - 1
        done = False
        found = False
        while not done and i0 < len(self.hull) - 1:
            if i0 == i1:
                done = True
            i_mid = (i0 + i1) // 2
            line_l = not is_ccw_turn(point, self.hull[i_mid], self.hull[0], )
            line_t = not is_ccw_turn(point, self.hull[i_mid + 1], self.hull[i_mid], )
            line_r = not is_ccw_turn(point, self.hull[0], self.hull[i_mid + 1], )
            # If satisfying the in_triangle_test, we have succeeded!
            if line_l and line_t and line_r:
                i0 = i_mid
                i1 = i_mid
                found = True
                done = True
            # If the top line ever causes a failure, we have lost by definition of a convex polygon.
            elif not line_t:
                done = True
            # If the point fails both the right and left tests, the point must be below the polygon.
            elif not line_l and not line_r:
                done = True
            # If none of the above apply, we must either move up or move down to lower the search space.
            elif line_l:
                i0 = i_mid + 1
            elif line_r:
                i1 = i_mid
            else:
                raise Exception("You have failed this program.")
        # If the point is ever below both sidelines, and not one or the other, it must be behind the origin.
        if not found:
            return None
        # If it is indeed within, get the ratios of the triangle areas, and use them to find the ratios of the paints
        else:
            a_origin = triangle_area(point, self.hull[i0], self.hull[i0 + 1])
            a_left = triangle_area(point, self.hull[0], self.hull[i0 + 1])
            a_right = triangle_area(point, self.hull[0], self.hull[i0])
            a_total = a_origin + a_left + a_right
            pairs = ((self.hull[0], a_origin), (self.hull[i0], a_left), (self.hull[i0 + 1], a_right))
            pairs = [(paint, area / a_total) for paint, area in pairs if area != 0]
            return pairs

    def add_points(self, points):
        new_hull = double_half_hull(points)



if __name__ == "__main__":
    class Test:
        def describe(self, *args, **kwargs):
            pass

        def expect(self, check):
            if not check:
                raise Exception("Test failed.")

    test = Test()

    def validate(paints_set, answer, target, validator):
        LEEWAY = 0.0001
        r_tot, g_tot = 0, 0
        if answer is None:
            test.expect(validator.validate(target) is None)
        else:
            for (r, g), f in answer:
                if (r, g) not in paints_set:
                    raise Exception("Used invalid color in answer: {}".format((r, g)))
                r_tot += r * f
                g_tot += g * f
            r_tar, g_tar = target
            test.expect(r_tot - LEEWAY < r_tar < r_tar + LEEWAY and
                        g_tot - LEEWAY < g_tar < g_tar + LEEWAY)

    from random import random
    DIVISIONS = 20

    validator = Easel()
    easel = Easel()
    for i in range(30):
        print("i: ", i)
        paints = {tuple([round(random(), 4) for k in range(2)]) for n in range(10)}
        easel.load_paints(list(paints))
        validator.load_paints(paints)
        for x in range(DIVISIONS):
            x = round(x / DIVISIONS, 4)
            for y in range(DIVISIONS):
                y = round(y / DIVISIONS, 4)
                res = easel.validate((x, y))
                print((x, y), res)
                validate(paints, res, (x, y), validator)
