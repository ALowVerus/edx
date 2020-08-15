from computational_geometry.b_tree_generic import RedBlackTree


class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __str__(self):
        return "({}, {})".format(self.x, self.y)


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


# Given three colinear points p, q, r, the function checks if
# point q lies on line segment 'pr'
def on_segment(p, q, r):
    if orientation(p, q, r) == 0 and \
            (q.x <= max(p.x, r.x)) and (q.x >= min(p.x, r.x)) and \
            (q.y <= max(p.y, r.y)) and (q.y >= min(p.y, r.y)):
        return True
    return False


class DynamicConvexHull:
    def __init__(self):
        pass

    def insert(self, p):
        pass

    def check(self, p):
        pass
