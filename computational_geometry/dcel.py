from cs1lib import *
import ctypes
import math
from collections import deque

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
    min_x, max_x = -1000, 1000
    min_y, max_y = -1000, 1000

    inserted_point_edge_color = (1, 0, 0)

    def __init__(self, points=None, is_voronoi=False):
        self.is_voronoi = is_voronoi
        self.outer = DCEL.Face()
        if points:
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
            vertices = [DCEL.Vertex(point) for point in points]
            lines = [DCEL.generate_half_edge_pair(vertices[i], vertices[(i + 1) % len(vertices)])
                     for i in range(len(vertices))]
            for i in range(len(lines)):
                phi_prev, rho_next = lines[(i - 1) % len(lines)]
                phi_curr, rho_curr = lines[i]
                phi_next, rho_prev = lines[(i + 1) % len(lines)]
                phi_curr.face = in_face
                rho_curr.face = self.outer
                phi_curr.succ = phi_next
                phi_curr.pred = phi_prev
                rho_curr.succ = rho_next
                rho_curr.pred = rho_prev
                phi_curr.color = (0.5, 0.5, 0.5)
                rho_curr.color = (0.5, 0.5, 0.5)
            in_face.inc = lines[0][0]
            self.outer.inc = lines[0][1]
            self.hashed_outer_border = {str(e) for e in self.outer.inc.linked_border}

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
            # The color of the line that is drawn when needed
            self.color = (0, 0, 0)

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
        def slope_theta(self):
            return math.atan2(self.dy, self.dx)

        @property
        def angle_theta(self):
            return DCEL.Vertex.angle_theta(self.pred.origin, self.origin, self.succ.origin)

        @property
        def linked_border(self):
            border = [self]
            curr = self.succ
            while curr is not self:
                border.append(curr)
                curr = curr.succ
            return border

        # Check for left turns in constant time
        @property
        def is_ccw_turn(self):
            return DCEL.is_ccw_turn(self.pred.origin, self.origin, self.succ.origin)

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
            x_adj = DCEL.line_side_offset * math.cos(self.slope_theta + math.pi / 2) * -1
            y_adj = DCEL.line_side_offset * math.sin(self.slope_theta + math.pi / 2) * -1

            set_stroke_color(0.5, 0.5, 0.5)
            draw_line(DCEL.scale_loc(self.p0.x), DCEL.scale_loc(self.p0.y),
                      DCEL.scale_loc(self.p1.x), DCEL.scale_loc(self.p1.y))

            x_short = DCEL.end_shortening * math.cos(self.slope_theta)
            y_short = DCEL.end_shortening * math.sin(self.slope_theta)
            scaled_p0_x = DCEL.scale_loc(self.p0.x) + x_adj + x_short
            scaled_p0_y = DCEL.scale_loc(self.p0.y) + y_adj + y_short
            scaled_p1_x = DCEL.scale_loc(self.p1.x) + x_adj - x_short
            scaled_p1_y = DCEL.scale_loc(self.p1.y) + y_adj - y_short

            head_angle = self.slope_theta + DCEL.arrow_head_angle
            head_end_x = scaled_p1_x - DCEL.arrow_head_len * math.cos(head_angle)
            head_end_y = scaled_p1_y - DCEL.arrow_head_len * math.sin(head_angle)

            r, g, b = self.color
            set_stroke_color(r, g, b)
            draw_line(scaled_p0_x, scaled_p0_y, scaled_p1_x, scaled_p1_y)
            draw_line(scaled_p1_x, scaled_p1_y, head_end_x, head_end_y)
            set_stroke_color(0, 0, 0)

        @classmethod
        def link_edges(cls, a, b):
            # Generate two new half-edges in the graph so as to enclose the newly-generated subspace
            pr, rp = DCEL.generate_half_edge_pair(a.origin, b.origin)
            # Insert on the helper
            a.pred.succ = pr
            pr.pred = a.pred
            a.pred = rp
            rp.succ = a
            # Insert on the new edge
            b.pred.succ = rp
            rp.pred = b.pred
            b.pred = pr
            pr.succ = b
            # Return the new edges for further manipulation
            return pr, rp

        def link_to_point(self, v):
            pr, rp = DCEL.generate_half_edge_pair(v, self.origin)
            pr.face = self.face
            rp.face = self.face
            rp.pred = self.pred
            self.pred.succ = rp
            pr.succ = self
            self.pred = pr
            v.inc = pr

        # Splice a target half-edge in after a given root
        @classmethod
        def splice_in_after(cls, r, t):
            r.succ.pred = t
            t.succ = r.succ
            r.succ = t
            t.pred = r

        def delete_edge_merge_faces(self, merge_faces=True):
            # Get the faces
            f0, f1 = self.face, self.twin.face
            # Link around the half-edges to be deleted
            self.pred.succ = self.twin.succ
            self.pred.succ.pred = self.pred
            self.succ.pred = self.twin.pred
            self.succ.pred.succ = self.succ
            # Set the origins to have valid initial lines
            self.origin.inc = self.twin.succ
            self.twin.origin.inc = self.succ
            print('O:', str(self.origin), str(self.origin.inc))
            print("T:", str(self.twin.origin), str(self.twin.origin.inc))
            # Return
            if merge_faces:
                new_face = DCEL.Face()
                new_face.inc = self.succ
                for edge in new_face.border:
                    edge.face = new_face
                del f0
                del f1
            else:
                new_face = None
            del self.twin
            del self
            if merge_faces:
                return new_face
            else:
                return f0, f1

    class Vertex:
        def __init__(self, point=(None, None)):
            self.y, self.x = point
            # The first outgoing incident half-edge
            self.inc = None
            # Provide a load spot
            self.load = None
            # Allow color to be set on the fly
            self.color = (0, 0, 0)

        def __str__(self):
            return "({},{})".format(round(self.y, 2), round(self.x, 2)) \
                if self.x is not None and self.y is not None else "None"

        @property
        def coord(self):
            return self.x, self.y

        @property
        def true_coord(self):
            return self.y, self.x

        @property
        def neighboring_faces(self):
            faces = [self.inc.face]
            curr = self.inc.pred.twin
            while curr != self.inc:
                faces.append(curr.face)
                curr = curr.pred.twin
            return faces

        @property
        def outgoing_edges(self):
            edges = [self.inc]
            curr = self.inc.pred.twin
            i = 0
            while curr != self.inc:
                if i > 1000:
                    raise Exception("You have a closed loop when looping for outgoing edges")
                i += 1
                edges.append(curr)
                curr = curr.pred.twin
            return edges

        # Taking in 3 points, output the area within them
        @staticmethod
        def triangle_area(p1, p2, p3):
            return abs((p1.x * (p2.y - p3.y) + p2.x * (p3.y - p1.y) + p3.x * (p1.y - p2.y))) / 2

        def draw(self):
            if (self.y, self.x) != (None, None):
                r, g, b = self.color
                set_stroke_color(r, g, b)
                set_fill_color(r, g, b)
                draw_circle(DCEL.scale_loc(self.x), DCEL.scale_loc(self.y), 3)
                set_font_size(15)
                set_stroke_color(r, g, b)
                set_fill_color(r, g, b)
                draw_text(str(self), DCEL.scale_loc(self.x), DCEL.scale_loc(self.y))

        # This method assumes that your angle proceeds from p0 to the fulcrum p1 to the end p2
        @classmethod
        def angle_theta(cls, p0, p1, p2):
            y_i, x_i = p0.y - p1.y, p0.x - p1.x
            y_f, x_f = p2.y - p1.y, p2.x - p1.x
            # print("({}, {}), (0, 0), ({}, {})".format(y_i, x_i, y_f, x_f))
            angle_i = math.atan2(y_i, x_i)
            angle_f = math.atan2(y_f, x_f)
            angle_t = angle_f - angle_i
            if angle_t < 0:
                angle_t += 2 * pi
            # print(list(map(lambda a: round(a * 180 / math.pi, 3), [angle_i, angle_f, angle_t])))
            return angle_t

        # Used to delete a vertex on the border. Only used when we know that it is on the border.
        def delete_border_vertex(self, designated_outside_face):
            created_border = []
            outgoing_edges = self.outgoing_edges
            for i in range(len(outgoing_edges)):
                curr = outgoing_edges[i].succ
                if curr.face != designated_outside_face:
                    while curr != outgoing_edges[i].pred:
                        created_border.append(curr)
                        curr = curr.succ
            try:
                matches = [created_border[i].succ.origin == created_border[i + 1].origin
                           for i in range(len(created_border) - 1)]
                i = matches.index(False)
                created_border = created_border[i+1:] + created_border[:i+1]
            except ValueError as exp:
                pass
            if not created_border:
                print('DELETING INLINE VERTEX:', str(self))
                created_border = [self.inc.twin.pred, self.inc.succ]
            else:
                created_border = [created_border[0].pred.twin.pred] + \
                                 created_border + \
                                 [created_border[-1].succ.twin.succ]
            print("CREATED BORDER:")
            for edge in created_border:
                print('\t', str(edge))
            for outgoing_edge in outgoing_edges:
                print("Killing", str(outgoing_edge))
                f0, f1 = outgoing_edge.delete_edge_merge_faces(merge_faces=False)
                if f0 is not designated_outside_face:
                    del f0
                if f1 is not designated_outside_face:
                    del f1
            print("After deleting inside edges", str(self))
            # Link the designated outside face to the appropriate new border
            designated_outside_face.inc = created_border[0]
            for edge in created_border:
                edge.face = designated_outside_face
            for i in range(len(created_border) - 1):
                created_border[i].succ = created_border[i + 1]
                created_border[i + 1].pred = created_border[i]
            print("After reconnecting the new border", str(self))
            for edge in created_border:
                print(str(edge))
                print(str(edge), [str(e) for e in edge.origin.outgoing_edges])

        @property
        def represents_infinity(self):
            return self.coord == (None, None)

    class Face:
        def __init__(self):
            # A reference to one of the edges of the face
            self.inc = None
            # A load that can be used for any number of things
            self.load = None
            # Track whether this face is or is not convex
            self.is_convex = False
            # Track color for the sake of the drawing functions
            self.color = (0, 0, 0)

        def __str__(self):
            return "F: [{}]".format(', '.join([str(coord) for coord in self.points]))

        def update_convexity(self):
            self.is_convex = True
            for edge in self.border:
                if edge.angle_theta > math.pi:
                    self.is_convex = False

        @property
        def border(self):
            return self.inc.linked_border

        @property
        def vertices(self):
            return [e.origin for e in self.border]

        @property
        def points(self):
            return [v.coord for v in self.vertices]

        @property
        def centroid(self):
            border = self.border
            centroid = DCEL.Vertex((sum([e.origin.y for e in border]) / len(border),
                                    sum([e.origin.x for e in border]) / len(border)))
            centroid.load = self
            return centroid

        def draw(self):
            r, g, b = self.color
            set_fill_color(r, g, b)
            set_stroke_color(r, g, b)
            edges = self.border
            points = []
            for i in range(len(edges)):
                # Get the 3 edges relevant to any particular turn
                pred, curr, succ = edges[(i - 1) % len(edges)], edges[i], edges[(i + 1) % len(edges)]
                # If the pred or succ represent infinity, ignore them, as they are added in the curr step
                if pred.origin.represents_infinity or succ.origin.represents_infinity:
                    pass
                # If the current origin doesn't represent infinity, add it to the points list as usual
                elif not curr.origin.represents_infinity:
                    points.append(curr.origin.coord)
                # If the current origin is indeed infinity, create new coordinates fitted to a finite display
                else:
                    # Get facial vertices, which correspond to Voronoi sites
                    l_face_vertex = pred.twin.face.load
                    c_face_vertex = curr.face.load
                    r_face_vertex = curr.twin.face.load

                    def get_theta(p1, p0):
                        theta = math.atan2(p1.y - p0.y, p1.x - p0.x)
                        theta += 2 * math.pi
                        while theta > 2 * math.pi:
                            theta -= 2 * math.pi
                        theta += math.pi / 2
                        while theta > 2 * math.pi:
                            theta -= 2 * math.pi
                        return theta

                    # Calculate the angles of the pred edge
                    theta_pred = get_theta(c_face_vertex, l_face_vertex)

                    # Calculate the angles of the succ edge
                    theta_succ = get_theta(r_face_vertex, c_face_vertex)

                    # Determine the end points of the two lines
                    def determine_intersection_with_limits(v, theta):
                        # if theta < 0:
                        #     theta += math.pi
                        # res = DCEL.Vertex((None, None))
                        # # Facing right
                        # if theta == 0 * math.pi / 2:
                        #     res.y, res.x = v.y, DCEL.max_x
                        # # Top right corner
                        # elif 0 * math.pi / 2 < theta < 1 * math.pi / 2:
                        #     max_x_intersection = (v.y + (DCEL.max_x - v.x) / math.tan(theta), DCEL.max_x)
                        #     max_y_intersection = (DCEL.max_y, v.y + (DCEL.max_y - v.y) / math.tan(theta))
                        # # Facing up
                        # elif theta == 1 * math.pi / 2:
                        #     res.y, res.x = DCEL.max_y, v.x
                        # # Top left corner
                        # elif 1 * math.pi / 2 < theta < 2 * math.pi / 2:
                        #     min_x_intersection = (0, DCEL.min_x)
                        #     max_y_intersection = (DCEL.max_y, v.y + (DCEL.max_y - v.y) / math.tan(theta))
                        # # Facing left
                        # elif theta == 2 * math.pi / 2:
                        #     res.y, res.x = v.y, DCEL.min_x
                        # # Bottom left corner
                        # elif 2 * math.pi / 2 < theta < 3 * math.pi / 2:
                        #     min_x_intersection = (v.y + (DCEL.min_x - v.x) / math.tan(theta), DCEL.min_x)
                        #     min_y_intersection = (DCEL.min_y, v.y + (DCEL.min_y - v.y) / math.tan(theta))
                        # # Facing down
                        # elif theta == 3 * math.pi / 2:
                        #     res.y, res.x = DCEL.min_y, v.x
                        # # Bottom right corner
                        # elif 4 * math.pi / 2 < theta < 4 * math.pi / 2:
                        #     max_x_intersection = (v.y + (DCEL.max_x - v.x) / math.tan(theta), DCEL.max_x)
                        #     min_y_intersection = (DCEL.min_y, 0)
                        # else:
                        #     raise Exception("You have an invalid angle. {}".format(theta))
                        # return res
                        return (v.y + math.cos(theta) * 100, v.x + math.sin(theta) * 100)

                    left_circle_coord = pred.origin.coord
                    left_border_coord = determine_intersection_with_limits(pred.origin, theta_pred)
                    right_border_coord = determine_intersection_with_limits(curr.twin.origin, theta_succ)
                    right_circle_coord = succ.origin.coord

                    points.extend([left_circle_coord, left_border_coord, right_border_coord, right_circle_coord])

            draw_polygon([[DCEL.scale_loc(n) for n in p] for p in points])
            set_fill_color(0, 0, 0)
            set_stroke_color(0, 0, 0)

        def insert_vertex(self, v):
            edges = self.border
            if len(edges) != 3:
                raise Exception("You're attempting to place a point in a non-triangle.")
            edges[0].link_to_point(v)
            outgoing = v.inc
            for border_edge in edges[1:]:
                DCEL.HalfEdge.link_edges(outgoing, border_edge)
                outgoing = outgoing.succ.succ.twin
            for edge in edges:
                new_face_border = edge.linked_border
                new_face = DCEL.Face()
                new_face.inc = edge
                for new_face_edge in new_face_border:
                    new_face_edge.face = new_face
                    new_face_edge.color = DCEL.inserted_point_edge_color
            del self
            return [edge.face for edge in edges]

        def contains_vertex(self, v):
            for edge in self.border:
                if not DCEL.is_ccw_turn(edge.origin, edge.succ.origin, v):
                    return False
            return True

    def generate_full_edge_list(self, including_outside=False):
        if type(self.outer) == DCEL.Face:
            q = [edge.twin for edge in self.outer.border]
            if including_outside:
                seen = set()
            else:
                seen = {id(edge) for edge in self.outer.border}
        elif type(self.outer) == DCEL.Vertex:
            q = [self.outer.inc]
            seen = set()
        else:
            raise Exception("You have an outer item of an invalid type.")
        edge_list = []
        while q:
            edge = q.pop()
            if id(edge) not in seen:
                edges_in_face = [edge]
                curr = edge.succ
                i = 0
                while curr != edge:
                    if curr.succ == curr:
                        raise Exception("You have an edge that succs itself. Please recheck you connection code. \n{}"
                                        .format(str(curr)))
                    i += 1
                    edges_in_face.append(curr)
                    curr = curr.succ
                for facial_edge in edges_in_face:
                    q.append(facial_edge)
                    q.append(facial_edge.twin)
                    seen.add(id(facial_edge))
                    edge_list.append(facial_edge)
        return edge_list

    def list_vertices(self):
        edges = self.generate_full_edge_list(True)
        vertices = []
        seen = set()
        for e in edges:
            if id(e.origin) not in seen:
                vertices.append(e.origin)
                seen.add(id(e.origin))
        return vertices

    def reflect(self):
        edge_list = self.generate_full_edge_list(including_outside=True)
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

    def list_faces(self, include_outside=False, verbose=False):
        edges = self.generate_full_edge_list(including_outside=include_outside)
        faces = []
        seen = set()
        for edge in edges:
            if verbose:
                print(str(edge), str(edge.face))
            face = edge.face
            if id(face) not in seen:
                seen.add(id(edge.face))
                faces.append(edge.face)
        return faces

    def reallocate_faces(self):
        q = [edge.twin for edge in self.outer.border]
        seen = {id(edge) for edge in self.outer.border}
        while q:
            edge = q.pop()
            if id(edge) not in seen:
                edges_in_face = edge.linked_border
                new_face = DCEL.Face()
                new_face.inc = edge
                for facial_edge in edges_in_face:
                    facial_edge.face = new_face
                    q.append(facial_edge.twin)
                new_face.update_convexity()
                seen.add(id(edge))

    @classmethod
    def generate_half_edge_pair_generic(cls, phi=Vertex(), rho=Vertex(), HalfEdgeClass=HalfEdge):
        pr = HalfEdgeClass()
        rp = HalfEdgeClass()
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
    def generate_half_edge_pair(cls, phi, rho):
        """
        Return a pair of edges from p0 to p1, with appropriate origin and twinning.
        """
        return DCEL.generate_half_edge_pair_generic(phi, rho, DCEL.HalfEdge)

    @classmethod
    def generate_half_edge_sequence_along_vertices(cls, list_of_vertices, is_circular=False):
        # Generate a list of edge pairs
        edge_pairs = []
        # Generate blank edge pairs for later use
        for i in range(len(list_of_vertices) - 1 + is_circular):
            phi, rho = list_of_vertices[i], list_of_vertices[(i + 1) % len(list_of_vertices)]
            pr, rp = DCEL.generate_half_edge_pair(phi, rho)
            edge_pairs.append((pr, rp))
        # Link the edge pairs to each other
        for i in range(len(edge_pairs) - 1 + is_circular):
            (pr, rp), (rt, tr) = edge_pairs[i], edge_pairs[(i + 1) % len(edge_pairs)]
            pr.succ = rt
            rt.pred = pr
            rp.pred = tr
            tr.succ = rp
        # Return the result
        return edge_pairs

    def draw(self):
        # Draw in turn the faces, edges, and vertices
        for face in self.list_faces():
            face.draw()
        if not self.is_voronoi:
            for line in self.generate_full_edge_list(True):
                line.draw()
            for line in self.generate_full_edge_list(True):
                line.origin.draw()
        else:
            set_stroke_color(0.5, 0.5, 0.5)
            for i in range(DCEL.wh_n):
                draw_line(DCEL.scale_loc(i), DCEL.min_y, DCEL.scale_loc(i), DCEL.max_y)
                draw_line(DCEL.min_x, DCEL.scale_loc(i), DCEL.max_x, DCEL.scale_loc(i))
            for face in self.list_faces():
                face.load.draw()

    def draw_dual(self):
        face_pairs = []
        seen_face_pairs = set()
        faces = self.list_faces()
        for f in faces:
            for e in f.border:
                if e.twin.face != self.outer:
                    k = tuple(sorted([f, e.twin.face], key=id))
                    if k not in seen_face_pairs:
                        seen_face_pairs.add(k)
                        face_pairs.append([f, e.twin.face])
        centroids = {id(face): face.centroid for face in faces}
        centroid_pairs = [[centroids[id(f0)], centroids[id(f1)]] for f0, f1 in face_pairs]
        edge_pairs = [DCEL.generate_half_edge_pair(c0, c1) for c0, c1 in centroid_pairs]
        for e0, e1 in edge_pairs:
            e0.draw()
            e1.draw()

    @classmethod
    def is_ccw_turn(cls, p0, p1, p2):
        return (p1.y - p0.y) * (p2.x - p0.x) - (p2.y - p0.y) * (p1.x - p0.x) >= 0

    # Copied math from http://ambrsoft.com/TrigoCalc/Circle3D.htm
    @classmethod
    def get_circle_from_three_points(cls, p0, p1, p2):
        a = [
            [p0.x, p0.y, 1],
            [p1.x, p1.y, 1],
            [p2.x, p2.y, 1],
        ]
        b = [
            [p0.x ** 2 + p0.y ** 2, p0.y, 1],
            [p1.x ** 2 + p1.y ** 2, p1.y, 1],
            [p2.x ** 2 + p2.y ** 2, p2.y, 1],
        ]
        c = [
            [p0.x ** 2 + p0.y ** 2, p0.x, 1],
            [p1.x ** 2 + p1.y ** 2, p1.x, 1],
            [p2.x ** 2 + p2.y ** 2, p2.x, 1],
        ]
        d = [
            [p0.x ** 2 + p0.y ** 2, p0.x, p0.y],
            [p1.x ** 2 + p1.y ** 2, p1.x, p1.y],
            [p2.x ** 2 + p2.y ** 2, p2.x, p2.y],
        ]

        def det(e):
            if len(e) == 2:
                return e[0][0] * e[1][1] - e[0][1] * e[1][0]
            elif len(e) == 3:
                det0 = det([[e[1][1], e[1][2]], [e[2][1], e[2][2]]]) * e[0][0]
                det1 = det([[e[1][0], e[1][2]], [e[2][0], e[2][2]]]) * e[0][1]
                det2 = det([[e[1][0], e[1][1]], [e[2][0], e[2][1]]]) * e[0][2]
                return det0 - det1 + det2
            else:
                raise Exception("Your matrix is not of size 2 or 3.")

        det_a, det_b, det_c, det_d = [det(e) for e in [a, b, c, d]]
        a, b, c, d = det_a, -det_b, det_c, -det_d
        if a == 0:
            raise Exception("You have provided three colinear points. {}, {}, {}".format(str(p0), str(p1), str(p2)))
        x = (-b) / (2 * a)
        y = (-c) / (2 * a)
        r = ((b ** 2 + c ** 2 - 4 * a * d) / (4 * a ** 2)) ** 0.5
        return x, y, r


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
