from collections import deque
from computational_geometry.s1_convex_hull.hull_methods_2d import is_ccw_turn
from computational_geometry.s4_voronoi.dcel import *


def generate_monotone_sections(polygon_points):
    """
    This function takes in a polygon and returns a list of sections monotone with respect to x.
    It also returns a list of the segments required to generate those sections from the input polygon.
    """
    # Organize the points by their x values.
    points = sorted(polygon_points)
    # Convert the points into a DCEL, for easy partitioning and addition of extra pieces during section-finding.
    # Generate a heap of stalagtites, i.e. those points which have both sides pointed onwards.
    """
    h = SegmentHeap()
    for v in vertices:
        top_line, bot_line = line to the right, line to the left
        if top_line and bot_line point inwards:
            add v to the heap of stalagitites to be managed
    """
    # Generate a BBST to hold in-progress sets.
    """
    class RedBlackSegmentSearchTree:
        def init
        def add_segment
        def remove_segment
    t = RedBlackSegmentSearchTree()
    """
    # While there are sections unprocessed...
    """
    while 
        # Approach the point with the lowest yet-unhit x
        seg = h.pop()
        # If a stalagtite is met, either generate a new BBST object or merge two existing objects.
        if seg is a stalagtite:
            merge the contained BBST object
            if there were BBST objects above / to the sides, complete one and merge the other into its place
        # If a stalagmite is met, either complete a BBST object or split into two new objects.
        elif seg is a stalagmite:
            generate a new section underneath the stalagmite
            if there was a section above it, split that section into two
        # If a non-stalagmite non-stalagtite is met, simply move on.
        else:
            pass and add a child to the heap
    """
    # Return a reference to a node on the hull of the polygon,
    # along with a list of all the inner items that must now be triangulated.
    return [], []


def monotone_x_triangulate(polygon_points, axis):
    """
    Given the in-order points of a polygon monotone with respect to x,
    return a list of edges required to triangulate it.
    """
    # Convert y-monotone sections into x-monotone sections, then reflect them over afterwards
    if axis == 'x':
        pass
    elif axis == 'y':
        pass
    else:
        raise Exception("Your axis is neither x nor y.")
    # Get a pointers to the start and end of this polygon, as well as pointers that we will use to track traversal
    min_index = polygon_points.index(min(polygon_points))
    max_index = polygon_points.index(max(polygon_points))
    # Get pointers for the top and bot sides.
    top_index = min_index + 1
    bot_index = min_index - 1
    # Generate linked list to act as a stack for unresolved points.
    q = deque()

    # Define two triangulating functions
    def resolve_left():
        if len(q) >= 3 and is_ccw_turn(q[-1], q[-2], q[-3]):
            while len(q) >= 3 and is_ccw_turn(q[-1], q[-2], q[-3]):
                # Remove the second-to-last point from the equation by forming a triangle with it as a point on the hull
                a = q.popleft()
                b = q.popleft()
                c = q.popleft()
                q.appendleft(c)
                q.appendleft(a)
            resolve_right()

    def resolve_right():
        if len(q) >= 3 and is_ccw_turn(q[0], q[1], q[2]):
            while len(q) >= 3 and is_ccw_turn(q[0], q[1], q[2]):
                # Remove the second-to-last point from the equation by forming a triangle with it as a point on the hull
                a = q.pop()
                b = q.pop()
                c = q.pop()
                q.append(c)
                q.append(a)
            resolve_left()
            
    # While not at the end of both chains...
    while top_index != max_index or bot_index != max_index:
        # Resolve the left side, which will naturally call the other side
        resolve_left()
        if polygon_points[top_index] <= polygon_points[bot_index]:
            q.appendleft(polygon_points[top_index])
            top_index += 1
        elif polygon_points[top_index] > polygon_points[bot_index]:
            q.appendleft(polygon_points[bot_index])
            bot_index += 1
    # Convert y-monotone sections into x-monotone sections, then reflect them over afterwards
    if axis == 'x':
        pass
    elif axis == 'y':
        pass
    else:
        raise Exception("Your axis is neither x nor y.")
    # Return your final answer
    return []


def triangulate(polygon_points):
    """
    This function takes in a list of points, assumed to be the in-order points of a certain unholed polygon.
    This polygon input may not be convex, nor even necessarily monotone.
    The function partitions the inputs into monotone sections, then triangulates those now monotone sections.
    The final result is a list of segments that will successfully triangulate the input polygon.
    """
    monotone_sections, segments = generate_monotone_sections(polygon_points)
    for monotone_section in monotone_sections:
        segments.extend()
    return []


def recursive_hull_triangulator(polygon_points):
    """
    Generates a triangulation of a bunch of unsorted points.
    Does not take into account existing connections between them.
    Works in O(nlogn) time, using the same method as merging two convex hulls.
    """
    # Sort points according to x so as to enable partitions.
    polygon_points = sorted(polygon_points)
    # Convert points into DCEL Vertex objects.
    dcel_points = [DCEL.Vertex(point) for point in polygon_points]
    # Define a function to recursively combine and triangulate between previously-validated hulls
    def recurse(points):
        if len(points) == 1:
            return points[0], points[0]
        elif len(points) == 2:
            ab = DCEL.HalfEdge()
            ab.origin = points[0]
            ba = DCEL.HalfEdge()
            ba.origin = points[1]
            ab.twin, ba.twin = ba, ab
            points[0].inc = ab
            points[1].inc = ba
            left, right = min(points, key=lambda p: p.coord), max(points, key=lambda p: p.coord)
            return left, right
        else:
            left_l, left_r = recurse(points[:len(points) // 2])
            right_l, right_r = recurse(points[len(points) // 2:])
            return left_l, right_r

    # Call the recursive function on all the points
    res = recurse(dcel_points)
    # Get the list of edges from the result
    return []


def dcel_to_simple_edge_list():
    """
    A function that converts a more complicated DCEL to a simple collection of edges.
    This allows the edges to be checked for correct triangulation.
    """
    pass
