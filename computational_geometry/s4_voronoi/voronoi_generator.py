from computational_geometry.dcel import DCEL
from heapq import heappop, heappush
from computational_geometry.s5_delauney import delauney
from cs1lib import *


def voronoi_generator_naive(points):
    """
    Construct a voronoi map using naive algorithm.
    Might make sense to traverse the map using DCEL twin links, so as to end up with a full DCEL when done.
    Has O(n^3) runtime.
    """
    # For each point, find its face's bounds
    for root_point in points:
        # Identify target points
        target_points = [point for point in points if point != root_point]
        # Initialize a face with infinite bounds
        face = DCEL.Face()
        # Break the initial face according to the first point
        """"""
        # Iteratively cut down on the face
        for target_point in target_points:
            # Generate lines bisecting the source with the target point
            """"""
            # Find the appropriate place to drop the target
                # Check each existing line for intersections with the incoming lines
    # Combine the parts into a voronoi map
    return voronoi_map


def voronoi_generator_incremental(points):
    """
    An incremental algorithm for generating a voronoi diagram.
    Generate a partial voronoi diagram, then add consecutive cells, cutting through the existing cells to do so.
    Seems to have runtime O(n^2 + nlogn) in the worst case, though the book says O(n^2 * logn).
    """
    return voronoi_map


def voronoi_generator_divide_and_conquer(points):
    """
    Essintially, order all points along the x-axis, then mergesert partial voronoi diagrams.
    The merge portion of this is exceedingly complex, and may require review.
    """
    return voronoi_map


def voronoi_generator_fortune(points):
    """
    A sweepline algorithm for generating voronoi diagrams.
    Uses two types of events: site events, which are pre-loaded, and circle events, which are generated.
    See Fortune's paper for details.
    """
    # Sort points according to x
    points = sorted(points)
    # Load up a heap with the requisite items
    heap = []
    for p in points:
        heappush(heap, (p, "Site", None))
    # Generate structures
    voronoi_map = None
    # While the heap exists, keep poppin
    while heap:
        point, event_type, ref = heappop(heap)

    return voronoi_map


def voronoi_generator_from_delauney(delauney_dcel):
    """
    See the title.
    """
    print()
    for site in delauney_dcel.list_vertices():
        print("Initial site:", str(site))
    print()

    # Generate a structure for holding the Voronoi vertices, and create getters / setters
    centroids = {}
    infinity_vertex = DCEL.Vertex((None, None))

    def get_centroid(vertices):
        key = tuple(sorted(vertices, key=lambda e: str(e)))
        return centroids[key] if key in centroids else infinity_vertex

    def set_centroid(vertices):
        # Create a stable key for the centroid
        key = tuple(sorted(vertices, key=lambda e: str(e)))
        if key in centroids:
            raise Exception("You're setting a centroid twice.")
        # If the face is not a triangle, you've fucked up.
        if len(vertices) != 3:
            raise Exception("You have an invalid number of vertices in your \"triangulation's\" faces.")
        v0, v1, v2 = vertices
        # Find the centroid for the face
        x, y, r = DCEL.get_circle_from_three_points(v0, v1, v2)
        # Store the centroid as a vertex
        centroid_vertex = DCEL.Vertex((x, y))
        # Store the centroid
        centroids[key] = centroid_vertex

    # Generate the centroids for each face in the Delauney triangulation.
    # Each face is associated with a single centroid.
    for face in delauney_dcel.list_faces():
        # Get a list of the vertices for this face
        vertices = face.vertices
        # Store a generated centroid
        set_centroid(vertices)
    # Generate a mirroring DCEL for the voronoi
    voronoi_dcel = DCEL(None, is_voronoi=True)
    # Generate a dictionary to hash the half-edges, so that they can later be linked
    valid_half_edge_dict = {}
    # Import the random function for color generation
    from random import random
    # Iterate over the sites to generate appropriate edges for each cell
    for site in delauney_dcel.list_vertices():
        print("\n\nProcessing", str(site))
        # Get a list of outgoing edges from this site
        site_edges = site.outgoing_edges
        # Determine whether the site is adjacent to the outside.
        site_is_unbounded = sum([e.face == delauney_dcel.outer for e in site_edges]) == 1
        # If the site is unbounded, rearrange the edges so that they are in order of ccw rotation about the border.
        if site_is_unbounded:
            site_edge_i = 0
            while site_edges[site_edge_i].twin.face != delauney_dcel.outer:
                site_edge_i += 1
            site_edges = site_edges[site_edge_i:] + site_edges[:site_edge_i]
        # Generate an empty face
        face = DCEL.Face()
        # Label the face with its appropriate site location
        face.load = site
        # Randomly color the face
        face.color = (random(), random(), random())
        # Generate half edges
        border_half_edges = [DCEL.HalfEdge() for border_edge_i in range(len(site_edges))]
        # Link up the border half edges
        for border_edge_i in range(len(border_half_edges)):
            border_half_edges[border_edge_i].succ = border_half_edges[(border_edge_i + 1) % len(border_half_edges)]
            border_half_edges[border_edge_i].pred = border_half_edges[(border_edge_i - 1) % len(border_half_edges)]
        # Define appropriate origins for each edge
        for site_edge_i in range(len(site_edges)):
            border_edge_i = site_edge_i
            border_half_edges[border_edge_i].origin = get_centroid(site_edges[site_edge_i].face.vertices)
            if border_half_edges[border_edge_i].origin is infinity_vertex:
                infinity_vertex.inc = border_half_edges[border_edge_i]
        # Link all half edges to the new face
        for border_half_edge in border_half_edges:
            border_half_edge.face = face
        # Link the face to its associated border
        face.inc = border_half_edges[0]
        # Hash the edges for later twinning
        for border_half_edge in border_half_edges:
            front, back = str(border_half_edge.origin), str(border_half_edge.succ.origin)
            if (front, back) in valid_half_edge_dict:
                raise Exception("You have duplicative half-edges. This should never happen.\n" +
                                "Failure is: {}".format((front, back)))
            else:
                valid_half_edge_dict[(front, back)] = border_half_edge
    # Using the hashed half edges, link up the borders of neighboring cells
    while valid_half_edge_dict:
        (front, back), e1 = valid_half_edge_dict.popitem()
        e2 = valid_half_edge_dict.pop((back, front))
        e1.twin = e2
        e2.twin = e1
    # Actually place the stuff in the Voronoi DCEL
    voronoi_dcel.outer = infinity_vertex
    # Return the completed voronoi diagram
    return voronoi_dcel


def voronoi_internal_area(voronoi_dcel):
    res = 0
    for face in voronoi_dcel.list_faces():
        edges = face.border
        if sum([str(e.origin) == "None" for e in edges]) == 0:
            for e in edges:
                p0, p1, p2 = face.load, e.origin, e.succ.origin
                res += DCEL.Vertex.triangle_area(p0, p1, p2)
    return res


if __name__ == "__main__":
    test_case = "random"
    if test_case == "random":
        from random import randint
        bound = 40
        points = list({(randint(0, bound), randint(0, bound)) for i in range(30)})
    elif test_case == "bounded_diamond":
        points = [(0, 0), (20, 0), (0, 20), (20, 20), (10, 10)]
    elif test_case == "unbounded_cross":
        points = [(0, 0), (20, 0), (0, 20), (20, 20)]
    elif test_case == "internal_square":
        points = [(0, 0), (20, 0), (0, 20), (20, 20)]
    elif test_case == "coinciding_points_error":
        points = [(5, 7), (28, 36), (19, 19), (35, 7), (39, 31), (1, 20), (20, 22), (12, 10), (12, 34), (38, 17), (16, 32), (13, 32), (9, 10), (3, 24), (25, 20), (18, 15), (13, 36), (30, 36), (34, 1), (0, 1), (21, 33), (29, 34), (14, 29), (3, 28), (13, 19), (14, 9), (30, 2), (33, 32), (36, 12), (14, 1)]
    else:
        raise Exception("You have selected an invalid test case.")

    print('Points:', sorted(points))

    delauney_dcel = delauney.delauney_randomized_incremental_constructor(points)
    voronoi_dcel = voronoi_generator_from_delauney(delauney_dcel)

    # Print the internal area of the voronoi diagram
    print(voronoi_internal_area(voronoi_dcel))

    DCEL.line_side_offset = 5
    DCEL.end_shortening = 20
    DCEL.wh_pixels = 800
    DCEL.adj = 100
    min_y, min_x = min([y for y, x in points]), min([x for y, x in points])
    max_y, max_x = max([y for y, x in points]), max([x for y, x in points])
    DCEL.wh_n = max([y for y, x in points] + [x for x, y in points])
    print("MinY, MinX, MaxY, MaxX", min_y, min_x, max_y, max_x, DCEL.wh_n)
    DCEL.readjust()

    def draw():
        voronoi_dcel.draw()

    start_graphics(draw, width=DCEL.wh_pixels, height=DCEL.wh_pixels)
