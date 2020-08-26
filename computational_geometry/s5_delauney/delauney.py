import numpy, ctypes
from computational_geometry.dcel import DCEL, obj
from computational_geometry.s1_convex_hull.hull_methods_2d import is_ccw_turn
from cs1lib import *
import math
from copy import deepcopy
from random import shuffle


def in_circle(a, b, c, p):
    matrix = [
        [a[0], a[1], a[0] ** 2 + a[1] ** 2, 1],
        [b[0], b[1], b[0] ** 2 + b[1] ** 2, 1],
        [c[0], c[1], c[0] ** 2 + c[1] ** 2, 1],
        [p[0], p[1], p[0] ** 2 + p[1] ** 2, 1],
    ]
    return numpy.linalg.det(matrix) > 0


def in_triangle(v0, v1, v2, p):
    return is_ccw_turn(v0.origin, v1.origin, p) and \
           is_ccw_turn(v1.origin, v2.origin, p) and \
           is_ccw_turn(v2.origin, v0.origin, p)


def delauney_randomized_incremental_constructor(points):
    """
    Generates a Delauney triangulation from a set of unsorted points.
    Generally: Create a randomized triangulation, then flip edges until a true triangulation is found.
    For point location, use simple buckets. It's O(n) to flip an edge, but as they are split, it approaches logn.
    There are nlogn rebucketings, each corresponding to a O(1) edge flip.
    """
    # Remove doubles.
    vertices = [DCEL.Vertex(p) for p in set(points)]
    # If there are fewer than 3 points, something is off. Write a custom edge-case algo for it.
    if len(points) < 3:
        return None
    # Get bounds for the enclosing set of points.
    min_x, max_x = min(vertices, key=lambda p: p.x).x,  max(vertices, key=lambda p: p.x).x
    dx = max_x - min_x
    min_y, max_y = min(vertices, key=lambda p: p.y).y,  max(vertices, key=lambda p: p.y).y
    dy = max_y - min_y
    # Generate an enclosing triangle to hold the Delauney triangulation.
    dcel = DCEL([(min_x - dx * 50 - 10, min_y - dy * 50 - 10),
                 (min_x - dx * 50 - 10, min_x + dy * 90 + 10),
                 (min_x + dx * 90 + 10, min_y - dy * 50 - 10)])
    in_face = dcel.outer.inc.twin.face
    in_face.load = vertices
    shuffle(in_face.load)
    # Load up a queue with references to unresolved faces.
    face_q = {str(in_face): in_face}
    print("Out face id:", id(dcel.outer), str(dcel.outer.inc))
    print("In face id:", id(in_face), str(in_face.inc))
    print("Initial contained faces:", [(id(face), str(face.inc)) for face in dcel.list_faces()])
    print("Load:", [(v.y, v.x) for v in in_face.load])

    def allocate_vertices_to_faces(vertices, sub_faces):
        for face in sub_faces:
            matching_vertices = [v for v in vertices if face.contains_vertex(v)]
            remaining_vertices = [v for v in vertices if not face.contains_vertex(v)]
            face.load = matching_vertices
            vertices = remaining_vertices
            print('FACIAL LOAD!', face.load)
        if len(vertices) > 0:
            raise Exception("You have propagated a vertex that fits in none of its available sub_faces.")

    print("\n\n\n")
    while face_q:
        # Pop a face to unload
        _, f = face_q.popitem()
        # If the face has vertices to assign
        if f and f.load:
            print("Next face to process:", id(f))
            try:
                print('Current faces in DCEL:', [(id(face), [str(item) for item in face.load]) for face in dcel.list_faces()])
            except AttributeError as e:
                print("Recieved an error while listing edges.", [(str(face)) for face in dcel.list_faces()])
            # Create a new vertex with assigned points in its associated sub_faces
            vertices = f.load
            f.load = []
            pivot = vertices.pop()
            print("Pivoting along", str(pivot), "within", str(f))
            print("Now have", len(dcel.list_faces()), "faces.", [str(item) for item in dcel.list_faces()])
            sub_faces = f.insert_vertex(pivot)
            print("Now have", len(dcel.list_faces()), "faces.", [str(item) for item in dcel.list_faces()])
            for sub_face in sub_faces:
                face_q[str(sub_face)] = sub_face
            allocate_vertices_to_faces(vertices, sub_faces)
            print("Vertices:", [str(v) for v in vertices])
            print("Allocations:")
            for sub_face in sub_faces:
                print('\t', str(sub_face), [str(v) for v in sub_face.load])

            def load_edge(d, e):
                d[str(e)] = d[str(e.twin)] = e

            def pop_edge(d):
                _, e = d.popitem()
                if str(e) in d:
                    d.pop(str(e))
                elif str(e.twin) in d:
                    d.pop(str(e.twin))
                else:
                    print("Not in d:", _, str(e))
                    print([item[0] for item in d.items()])
                    raise Exception("You have somehow fricked up.")
                return e

            # If the sub_faces can be optimized, and edge flipping is merited, engage in edge flipping
            edge_q = {}
            for e in pivot.outgoing_edges:
                load_edge(edge_q, e.succ)
            while edge_q:
                e = pop_edge(edge_q)
                print('Considering', e, e.face, e.face.load, e.twin, e.twin.face, e.twin.face.load)
                if str(e) in dcel.hashed_outer_border or str(e.twin) in dcel.hashed_outer_border:
                    print('\tThis edge is on the border.')
                else:
                    # Get the four relevant points
                    a = e.succ.succ.origin
                    b = e.origin
                    c = e.twin.pred.origin
                    d = e.succ.origin
                    # Confirm that a flipping is possible
                    if not DCEL.is_ccw_turn(c, a, b) or not DCEL.is_ccw_turn(a, c, d):
                        print("Cannot flip due to invalid angles.")
                    else:
                        rho_ab = DCEL.Vertex.angle_theta(b, c, a)
                        rho_bc = DCEL.Vertex.angle_theta(c, a, b)
                        rho_cd = DCEL.Vertex.angle_theta(d, a, c)
                        rho_da = DCEL.Vertex.angle_theta(a, c, d)
                        phi_ab = DCEL.Vertex.angle_theta(b, d, a)
                        phi_bc = DCEL.Vertex.angle_theta(c, d, b)
                        phi_cd = DCEL.Vertex.angle_theta(d, b, c)
                        phi_da = DCEL.Vertex.angle_theta(a, b, d)
                        if rho_ab > phi_ab and rho_bc > phi_bc and rho_cd > phi_cd and rho_da > phi_da:
                            try:
                                vertices = e.face.load + e.twin.face.load
                                side_0, side_1 = e.pred, e.twin.pred
                                if str(side_0.face) in face_q:
                                    face_q.pop(str(side_0.face))
                                if str(side_1.face) in face_q:
                                    face_q.pop(str(side_1.face))
                                e.delete_edge_merge_faces()
                                pr, rp = DCEL.HalfEdge.link_edges(side_0, side_1)
                                pr.color = rp.color = (1, 0, 0)
                                face_0, face_1 = DCEL.Face(), DCEL.Face()
                                face_0.inc = side_0
                                face_1.inc = side_1
                                for edge_0 in side_0.linked_border:
                                    edge_0.face = face_0
                                for edge_1 in side_1.linked_border:
                                    edge_1.face = face_1
                                sub_faces = [pr.face, rp.face]
                                allocate_vertices_to_faces(vertices, sub_faces)
                                face_q[str(face_0)] = face_0
                                face_q[str(face_1)] = face_1
                                load_edge(edge_q, pr.succ)
                                load_edge(edge_q, rp.succ)
                                load_edge(edge_q, pr.pred)
                                load_edge(edge_q, rp.pred)
                            except TypeError as exp:
                                print("You've failed to flip. Interrupting." +
                                      str([id(g.face) for g in e.linked_border]))
                                raise exp
                        else:
                            pass
            print("\n\n\n")
    print("DONE TRIANGULATING! Now to get rid of the border.\n\n")
    # Remove the border vertices and create a new border
    for border_vertex in dcel.outer.vertices:
        print("Deleting", str(border_vertex))
        border_vertex.delete_border_vertex(designated_outside_face=dcel.outer)
    # Return a reference to the enclosing triangle.
    return dcel


def delauney_generator_from_voronoi(voronoi_graph):
    """
    Generates a Delauney triangulation from the voronoi graph in linear time.
    Generate an edge from each bisector of each voronoi edge.
    """
    return None


def gabriel_generator(delauney_dcel):
    """
    Generate a Gabriel subgraph from the delauney triangulation. Remove every edge where a succ/pred has an acute angle.
    And leads to a point within the containing circle.
    """
    # Get a list of non-duplicative edges
    edge_dict = {}
    for edge in delauney_dcel.generate_full_edge_list(including_outside=True):
        edge_dict[max([str(edge), str(edge.twin)])] = edge
    edges = [v for k, v in edge_dict.items()]

    # Define what it means to be invalid
    def is_invalid(c0, c1, p):
        y_mid, x_mid = (c1.y - c0.y) / 2, (c1.x - c0.x) / 2
        r_max_2 = ((c1.y - y_mid) ** 2 + (c1.x - x_mid) ** 2)
        r_point_2 = ((p.y - y_mid) ** 2 + (p.x - x_mid) ** 2)
        return r_max_2 <= r_point_2

    # Remove edges which have neighbors inside their circumcircles
    for edge in edges:
        if (edge.is_ccw_turn and is_invalid(edge.origin, edge.succ.origin, edge.pred.origin)) or \
                (edge.twin.is_ccw_turn and is_invalid(edge.twin.origin, edge.twin.succ.origin, edge.twin.pred.origin)):
            # Kill the invalid edge
            edge.delete_edge_merge_faces(False)
            edge.delete_edge_merge_faces(False)
            # Link shit up
            pass


def relative_neighborhood_generator(gabriel_dcel):
    """
    Generate a relative neighbor subgraph from the Gabriel subgraph. Unsure of how to handle this.
    """
    return None


def euclidean_minimum_spanning_tree_generator(relative_neighborhood_graph):
    """
    Generate a minimum spanning tree for this graph. Note that the EMST is a subgraph of the RNG.
    Unsure of how to implement this one.
    """
    return None


def euclidean_travelling_salesman(euclidean_minimum_spanning_tree):
    """
    From the minimum spanning tree, generate a travelling salesman solution.
    Starting from any random node, travel left, doubling back when you hit a dead end.
    Any newly-hit node is added to the traversal path, and any multi-hit node is ignored and passed by.
    This cannot possibly be over 2x the length of the best possible EST solution.
    """
    return None


if __name__ == "__main__":
    test_case = "random"
    if test_case == "simple_tri":
        points = [(5, 5), (20, 20), (15, 2)]
    elif test_case == "simple_quad":
        points = [(2, 10), (20, 20), (15, 2), (7, 3)]
    elif test_case == "simple_pent":
        points = [(5, 5), (20, 20), (15, 2), (7, 3), (12, 13)]
    elif test_case == "error_1":
        points = [(12, 27), (29, 27), (40, 29), (27, 6), (6, 25), (21, 23)]
    elif test_case == "line_1":
        points = [(10, 0), (5, 5), (0, 10)]
    elif test_case == "line_2":
        points = [(0, 0), (5, 5), (10, 10)]
    elif test_case == "none_generator":
        points = [(25, 37), (32, 20), (9, 31), (39, 23), (19, 14), (22, 22), (34, 39), (21, 30), (32, 35), (5, 23), (38, 28), (9, 23), (36, 17), (30, 10), (15, 16), (7, 37), (37, 23), (20, 30), (9, 14), (31, 17), (21, 11), (39, 28), (16, 23), (11, 0), (25, 36), (33, 16), (6, 8), (7, 30), (9, 9), (21, 19)]
    elif test_case == "coinciding_points_error":
        points = [(5, 7), (39, 31), (9, 10), (30, 2), (29, 34), (12, 10), (34, 1), (18, 15), (20, 22), (13, 32), (36, 12), (3, 28), (21, 33), (35, 7), (1, 20), (3, 24), (33, 32), (14, 9), (14, 1), (12, 34), (25, 20), (14, 29), (38, 17), (13, 19), (19, 19), (16, 32), (13, 36), (28, 36), (0, 1), (30, 36)]
    elif test_case == "random":
        from random import randint
        count = 6
        bound = 40
        points = list({(randint(0, bound), randint(0, bound)) for i in range(count)})
    else:
        points = [(0, 0)]

    print('\nPoints: {}\n'.format(str(points)))
    dcel = delauney_randomized_incremental_constructor(points)
    print("Final dcel faces:", dcel.list_faces())

    DCEL.line_side_offset = 5
    DCEL.end_shortening = 20
    DCEL.wh_pixels = 900
    DCEL.adj = 100
    min_y, min_x = min([y for y, x in points]), min([x for y, x in points])
    max_y, max_x = max([y for y, x in points]), max([x for y, x in points])
    DCEL.wh_n = max([y for y, x in points] + [x for x, y in points])
    print("MinY, MinX, MaxY, MaxX", min_y, min_x, max_y, max_x, DCEL.wh_n)
    DCEL.readjust()

    def draw():
        dcel.draw()
    start_graphics(draw, width=DCEL.wh_pixels, height=DCEL.wh_pixels)
