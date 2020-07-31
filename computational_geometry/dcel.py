from cs1lib import *
import ctypes
import math

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


class DCEL:
    adj = 5
    wh_pixels = 500
    wh_n = 90
    line_side_offset = 0
    arrow_head_angle = math.pi / 16
    arrow_head_len = 20
    end_shortening = 10
    scalar = (wh_pixels - adj * 2) / wh_n

    @classmethod
    def readjust(cls):
        DCEL.scalar = (DCEL.wh_pixels - DCEL.adj * 2) / DCEL.wh_n

    @classmethod
    def scale_loc(cls, n):
        return n * DCEL.scalar + DCEL.adj

    @classmethod
    def descale_loc(cls, n):
        return (n - DCEL.adj) / DCEL.scalar

    class HalfEdge:
        def __init__(self):
            # The corresponding half-edge, on the opposite side & direction
            self.twin = None
            # The point front which the half-edge proceeds
            self.origin = None
            # The face to the left
            self.face = None
            # The line preceding this one along the border of its left face
            self.pred = None
            # The line succeeding this one along the border of its left face
            self.succ = None

        @property
        def p0(self):
            return self.origin

        @property
        def p1(self):
            return self.succ.origin

        @property
        def dy(self):
            return self.p1.y - self.p0.y

        @property
        def dx(self):
            return self.p1.x - self.p0.x

        @property
        def theta(self):
            return math.atan2(self.dy, self.dx)

        # Check for left turns in constant time
        @property
        def is_ccw_turn(self):
            p0, p1, p2 = self.pred.origin, self.origin, self.succ.origin
            return (p1.y - p0.y) * (p2.x - p0.x) - (p2.y - p0.y) * (p1.x - p0.x) > 0

        def __str__(self):
            return "[{}, {}]".format(str((self.p0.y, self.p0.x)), str((self.p1.y, self.p1.x)))

        def plot(self, x):
            dy, dx = self.dy, self.dx
            if dx == 0:
                raise Exception('Attempting to plot on a line with no dx.')
            else:
                m = dy / dx
                b = self.p0.y - m * self.p0.x
                y = m * x + b
                return y

        # Draw a line using the CS1 library, appropriately scaling the image according to the DCEL parameters
        def draw(self):
            x_adj = DCEL.line_side_offset * math.cos(self.theta + math.pi / 2) * -1
            y_adj = DCEL.line_side_offset * math.sin(self.theta + math.pi / 2) * -1

            set_stroke_color(0.5, 0.5, 0.5)
            draw_line(DCEL.scale_loc(self.p0.x), DCEL.scale_loc(self.p0.y),
                      DCEL.scale_loc(self.p1.x), DCEL.scale_loc(self.p1.y))

            x_short = DCEL.end_shortening * math.cos(self.theta)
            y_short = DCEL.end_shortening * math.sin(self.theta)
            scaled_p0_x = DCEL.scale_loc(self.p0.x) + x_adj + x_short
            scaled_p0_y = DCEL.scale_loc(self.p0.y) + y_adj + y_short
            scaled_p1_x = DCEL.scale_loc(self.p1.x) + x_adj - x_short
            scaled_p1_y = DCEL.scale_loc(self.p1.y) + y_adj - y_short

            set_stroke_color(0, 0, 0)
            draw_line(scaled_p0_x, scaled_p0_y, scaled_p1_x, scaled_p1_y)

            head_angle = self.theta + DCEL.arrow_head_angle
            head_end_x = scaled_p1_x - DCEL.arrow_head_len * math.cos(head_angle)
            head_end_y = scaled_p1_y - DCEL.arrow_head_len * math.sin(head_angle)

            set_stroke_color(0, 0, 0)
            draw_line(scaled_p1_x, scaled_p1_y, head_end_x, head_end_y)

    class Vertex:
        def __init__(self, point):
            self.y, self.x = point
            # The first outgoing incident half-edge
            self.inc = None

        def __str__(self):
            return "({},{})".format(round(self.y, 2), round(self.x, 2))

        # Taking in 3 points, output the area within them
        @staticmethod
        def triangle_area(p1, p2, p3):
            return abs((p1.x * (p2.y - p3.y) + p2.x * (p3.y - p1.y) + p3.x * (p1.y - p2.y))) / 2

        def draw(self):
            draw_circle(DCEL.scale_loc(self.x), DCEL.scale_loc(self.y), 3)
            set_font_size(15)
            draw_text(str(self), DCEL.scale_loc(self.x), DCEL.scale_loc(self.y))

    class Face:
        def __init__(self):
            # A reference to one of the edges of the face
            self.inc = None
            # A load that can be used for any number of things
            self.load = None

        @property
        def border(self):
            border = [self.inc]
            curr = self.inc.succ
            while curr is not self.inc:
                border.append(curr)
                curr = curr.succ
            return border

        def generate_full_edge_list_from_outer_face(self, including_outside=False):
            q = [edge.twin for edge in self.border]
            if including_outside:
                seen = set()
            else:
                seen = {id(edge) for edge in self.border}
            edge_list = []
            while q:
                edge = q.pop()
                if id(edge) not in seen:
                    edges_in_face = [edge]
                    curr = edge.succ
                    while curr != edge:
                        edges_in_face.append(curr)
                        curr = curr.succ
                    new_face = DCEL.Face()
                    new_face.inc = edge
                    for facial_edge in edges_in_face:
                        facial_edge.face = new_face
                        q.append(facial_edge)
                        seen.add(id(facial_edge))
                        edge_list.append(facial_edge)
            return edge_list

        def reallocate_faces_from_outer_face(self):
            q = [edge.twin for edge in self.border]
            seen = {id(edge) for edge in self.border}
            while q:
                edge = q.pop()
                if id(edge) not in seen:
                    edges_in_face = [edge]
                    curr = edge.succ
                    while curr != edge:
                        edges_in_face.append(curr)
                        curr = curr.succ
                    new_face = DCEL.Face()
                    new_face.inc = edge
                    for facial_edge in edges_in_face:
                        facial_edge.face = new_face
                        q.append(facial_edge)
                    seen.add(id(edge))

        def list_contained_faces_from_outer_face(self):
            edges = self.generate_full_edge_list_from_outer_face()
            faces = []
            seen = set()
            for edge in edges:
                if id(edge.face) not in seen:
                    seen.add(id(edge.face))
                    faces.append(edge.face)
            return faces

        def reflect(self):
            print("Reflected polygon.")
            edge_list = self.generate_full_edge_list_from_outer_face(including_outside=True)
            edge_list = sorted(edge_list, key=lambda e: (e.origin.y, e.origin.x))
            vertices_list = [edge.origin for edge in edge_list]
            seen = set()
            vertices_set = []
            for vertex in vertices_list:
                if id(vertex) not in seen:
                    seen.add(id(vertex))
                    vertices_set.append(vertex)
            for vertex in vertices_set:
                vertex.x *= -1
                vertex.y *= -1

    @classmethod
    def generate_half_edge_pair(cls, phi, rho):
        """
        Return a pair of edges from p0 to p1, with appropriate origin and twinning.
        """
        pr = DCEL.HalfEdge()
        rp = DCEL.HalfEdge()
        pr.twin = rp
        rp.twin = pr
        pr.origin = phi
        rp.origin = rho
        pr.succ = rp
        rp.succ = pr
        pr.pred = rp
        rp.pred = pr
        phi.inc = pr
        rho.inc = rp
        return pr, rp

    @classmethod
    def generate_dcel_from_coordinates_list(cls, points):
        # Ensure that the points are in CCW order
        min_point = min(points)
        i = points.index(min_point)
        a, b, c = points[(i - 1) % len(points)], points[i], points[(i + 1) % len(points)]
        (ay, ax), (by, bx), (cy, cx) = a, b, c
        det = (by * ax + ay * cx + cy * bx) - (ay * bx + by * cx + cy * ax)
        print("Points det at {}, {}, {} juncture is {}.".format(a, b, c, det))
        if det > 0:
            points = points[::-1]
        print("Making a CCW DCEL from points", points)
        # Generate a DCEL with two faces, one in, one out
        in_face = DCEL.Face()
        out_face = DCEL.Face()
        vertices = [DCEL.Vertex(point) for point in points]
        lines = [DCEL.generate_half_edge_pair(vertices[i], vertices[(i + 1) % len(vertices)])
                 for i in range(len(vertices))]
        for i in range(len(lines)):
            phi_prev, rho_next = lines[(i - 1) % len(lines)]
            phi_curr, rho_curr = lines[i]
            phi_next, rho_prev = lines[(i + 1) % len(lines)]
            phi_curr.face = in_face
            rho_curr.face = out_face
            phi_curr.succ = phi_next
            phi_curr.pred = phi_prev
            rho_curr.succ = rho_next
            rho_curr.pred = rho_prev
        in_face.inc = lines[0][0]
        out_face.inc = lines[0][1]
        # Return a reference to the inner face
        return out_face


framework = "finding_monotone_parts"

if __name__ == "__main__":
    if framework == "merging_triangulations":
        """
        l_max_i, r_min_i 1 0
        Top: 1 1
        Bot: 2 0

        lh: [[1, 1], [2, 7], [1, 19]]
        rh: [[2, 74], [4, 19], [6, 52], [7, 74]]
        """
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
        lgon = DCEL.generate_dcel_from_coordinates_list(lh)
        rgon = DCEL.generate_dcel_from_coordinates_list(rh)


        def draw():
            for line in lgon + rgon:
                line.draw()
            for point in points:
                point.draw()
            # top_line.draw()
            # bot_line.draw()
            # starting_line.draw()


        start_graphics(draw)
    elif framework == "finding_monotone_parts":
        pass
