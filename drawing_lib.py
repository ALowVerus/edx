from cs1lib import *
import ctypes

adj = 20
wh_pixels = 500
wh_n = 10
scalar = (wh_pixels - adj * 2) / wh_n


COLORS = [
    (0, 0, 1),
    (0, 1, 0),
    (1, 0, 0),
    (1, 1, 0),
    (1, 0, 1),
    (0, 1, 1),
    (0.5, 0.5, 0.5),
    (0.5, 0.5, 0),
    (0.5, 0, 0.5),
    (0, 0.5, 0.5),
    (0, 0, 0.5),
    (0, 0.5, 0),
    (0.5, 0, 0),
]


def obj(n):
    return ctypes.cast(n, ctypes.py_object).value


def scale_loc(n):
    return n * scalar + adj


def descale_loc(n):
    return (n - adj) / scalar


# Define a point class to hold point data
class Point:
    def __init__(self, y, x):
        self.y = y
        self.x = x
        self.lines = set()

    def __str__(self):
        return "({},{})".format(self.y, self.x)

    # Taking in 3 points, output the area within them
    @staticmethod
    def triangle_area(p1, p2, p3):
        return abs((p1.x * (p2.y - p3.y) + p2.x * (p3.y - p1.y) + p3.x * (p1.y - p2.y))) / 2

    def draw(self):
        draw_circle(scale_loc(self.x), scale_loc(self.y), 3)


# Define a line class to hold
class Line:
    def __init__(self, p0, p1):
        if type(p0) is not Point:
            p0 = Point(p0[0], p0[1])
        if type(p1) is not Point:
            p1 = Point(p1[0], p1[1])
        if p0.x != p1.x:
            self.points = sorted([p0, p1], key=lambda p: p.x)
        else:
            self.points = sorted([p0, p1], key=lambda p: p.y)
        self.p0.lines.add(id(self))
        self.p1.lines.add(id(self))

    @property
    def p0(self):
        return self.points[0]

    @property
    def p1(self):
        return self.points[1]

    def __str__(self):
        return "[{}, {}]".format(str(self.p0), str(self.p1))

    def plot(self, x):
        m = (self.p1.y - self.p0.y) / (self.p1.x - self.p0.x)
        b = self.p0.y - m * self.p0.x
        y = m * x + b
        return y

    def draw(self):
        draw_line(
            scale_loc(self.p0.x), scale_loc(self.p0.y),
            scale_loc(self.p1.x), scale_loc(self.p1.y)
        )


def generate_polygon(points):
    if type(points[0]) is not Point:
        points = [Point(x, y) for x, y in points]
    lines = [Line(points[i], points[(i+1) % len(points)]) for i in range(len(points))]
    return lines


"""
l_max_i, r_min_i 1 0
Top: 1 1
Bot: 2 0

lh: [[1, 1], [2, 7], [1, 19]]
rh: [[2, 74], [4, 19], [6, 52], [7, 74]]
"""


if __name__ == "__main__":
    points = [[2, 7], [4, 19], [2, 74], [6, 52], [1, 19], [7, 74], [1, 1]]
    lh = [[1, 1], [2, 7], [1, 19]]
    rh = [[2, 74], [4, 19], [6, 52], [7, 74]]
    l_max_i, r_min_i = 1, 0
    bot_i_l, bot_i_r = 2, 0
    top_i_l, top_i_r = 1, 1
    points = [Point(x * 5, y / 3) for x, y in points]
    lh = [(x * 5, y / 3) for x, y in lh]
    rh = [(x * 5, y / 3) for x, y in rh]
    starting_line = Line(lh[l_max_i], rh[r_min_i])
    top_line = Line(lh[top_i_l], rh[top_i_r])
    bot_line = Line(lh[bot_i_l], rh[bot_i_r])
    lgon = generate_polygon(lh)
    rgon = generate_polygon(rh)
    def draw():
        for line in lgon + rgon:
            line.draw()
        for point in points:
            point.draw()
        top_line.draw()
        bot_line.draw()
        starting_line.draw()
    start_graphics(draw)
