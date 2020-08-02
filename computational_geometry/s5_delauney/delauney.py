import numpy, ctypes
from computational_geometry.dcel import DCEL, obj
from computational_geometry.s1_convex_hull.hull_methods_2d import is_ccw_turn


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
    points = [DCEL.Vertex(p) for p in set(points)]
    # If there are fewer than 3 points, something is off. Write a custom edge-case algo for it.
    if len(points) < 3:
        return None
    # Get bounds for the enclosing set of points.
    min_x, max_x = min(points, key=lambda p: p.x).x,  max(points, key=lambda p: p.x).x
    min_y, max_y = min(points, key=lambda p: p.y).y,  max(points, key=lambda p: p.y).y
    # Generate an enclosing triangle to hold the Delauney triangulation.
    outer_face = DCEL.generate_dcel_from_coordinates_list(
        [(min_x-5, min_y-5), (min_x-5, min_x+(max_y-min_y)*2+20), (min_x+(max_x-min_x)*2+20, min_y-5)])
    initial_face = outer_face.inc.twin.face
    initial_face.load = points
    # Load up a queue with references to unresolved faces.
    q = {id(initial_face)}
    while q:
        # Grab a face from the queue
        face = obj(q.pop())
        points = face.load
        # If the load is 0, we're done.
        if len(points) == 0:
            pass
        # Otherwise, we need to allocate points and flip edges.
        else:
            new_edges = [face.inc, face.inc.succ, face.inc.succ.succ]
            # Select a random point to use as a target
            vertex = DCEL.Vertex(points.pop())
            # Generate new triangles from the point. Account for the vertex being on the line of an existing triangle.
            for phi in new_edges:
                de_phi_o, ad_phi_o = DCEL.generate_half_edge_pair(vertex, phi.origin)
                vertex.inc = ad_phi_o
                phi.prev = ad_phi_o
                ad_phi_o.succ = phi
            for phi in new_edges:
                phi.succ = phi.prev.twin
                phi.succ.prev = phi
                phi.prev.prev = phi.succ
                phi.succ.succ = phi.prev
            # Generate faces with subsets of points for each of the three new triangles.
            for phi in new_edges:
                a, b, c = phi, phi.succ, phi.succ.succ
                sub_face = DCEL.Face()
                sub_face.inc = a
                a.face = sub_face
                b.face = sub_face
                c.face = sub_face
                sub_face.load = []
                failed_points = []
                for point in points:
                    if in_triangle(a, b, c):
                        sub_face.load.append(point)
                    else:
                        failed_points.append(point)
                points = failed_points
            if len(points) > 0:
                raise Exception("You have been unable to place a number of points within any sub-triangle.")
            # Generate a queue of possible edge flips. Enqueue newly-created sub-triangles.
            seen_edges = set()
            edge_q = new_edges
            while edge_q:
                edge = edge_q.pop()
                seen_edges.add(id(edge))

    # Return a reference to the enclosing triangle.
    return a


def delauney_generator_from_voronoi(voronoi_graph):
    """
    Generates a Delauney triangulation from the voronoi graph in linear time.
    Generate an edge from each bisector of each voronoi edge.
    """
    return None


def gabriel_generator(delauney_graph):
    """
    Generate a Gabriel subgraph from the delauney triangulation. Remove every edge where a succ/pred has an acute angle.
    And leads to a point within the containing circle.
    """
    return None


def relative_neighborhood_generator(gabriel_graph):
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
    # for p in [(5, 5), (20, 20), (15, 2), (20, 10)]:
    #     print(p, in_circle((10, 10), (17, 5), (6, 19), p))
    print(delauney_randomized_incremental_constructor([(5, 5), (20, 20), (15, 2), (20, 10)]))
