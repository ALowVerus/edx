from computational_geometry.s4_voronoi.dcel import DCEL
from heapq import heappop, heappush


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
    # Generate structures to enable 
    # While the heap exists, keep poppin
    while heap:
        point, attr = heappop(heap)

    return voronoi_map


if __name__ == "__main__":
    from random import randint
    bound = 40
    points = list({(randint(0, bound), randint(0, bound)) for i in range(30)})
    voronoi_map = voronoi_generator_naive(points)
