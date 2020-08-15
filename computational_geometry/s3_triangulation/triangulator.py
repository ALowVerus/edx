from collections import deque
from computational_geometry.s1_convex_hull.hull_methods_2d import is_ccw_turn
from computational_geometry.dcel import *
from computational_geometry.b_tree_generic import RedBlackTree
from cs1lib import *


is_source = lambda e: e.dx >= 0 and e.pred.dx < 0 and e.is_ccw_turn
is_sink = lambda e: e.dx < 0 and e.pred.dx >= 0 and e.is_ccw_turn
is_l_progress = lambda e: e.dx < 0 and e.pred.dx < 0
is_r_progress = lambda e: e.dx >= 0 and e.pred.dx >= 0
is_stalagmite = lambda e: e.dx >= 0 and e.pred.dx < 0 and not e.is_ccw_turn
is_stalactite = lambda e: e.dx < 0 and e.pred.dx >= 0 and not e.is_ccw_turn


def generate_monotone_sections(dcel):
    """
    This function takes in a polygon and returns a list of sections monotone with respect to x.
    It also returns a list of the segments required to generate those sections from the input polygon.
    """
    # Get the initial inner face
    inner_face = dcel.list_faces()[0]
    inner_face_edges = inner_face.border

    sources = [edge for edge in inner_face_edges if is_source(edge)]
    sinks = [edge for edge in inner_face_edges if is_sink(edge)]
    l_progress = [edge for edge in inner_face_edges if is_l_progress(edge)]
    r_progress = [edge for edge in inner_face_edges if is_r_progress(edge)]
    stalagmites = [edge for edge in inner_face_edges if is_stalagmite(edge)]
    stalactites = [edge for edge in inner_face_edges if is_stalactite(edge)]

    print(len(sources), "sources")
    print(len(sinks), "sinks")
    print(len(l_progress), "l_prog")
    print(len(r_progress), "r_prog")
    print(len(stalagmites), "stalagmites")
    print(len(stalactites), "stalactites")

    sources_ids = {id(edge) for edge in sources}
    sinks_ids = {id(edge) for edge in sinks}
    l_progress_ids = {id(edge) for edge in l_progress}
    r_progress_ids = {id(edge) for edge in r_progress}
    stalagmites_ids = {id(edge) for edge in stalagmites}
    stalactites_ids = {id(edge) for edge in stalactites}

    for edge in inner_face_edges:
        if sum([id(edge) in l for l in [sources_ids, sinks_ids,
                                        l_progress_ids, r_progress_ids,
                                        stalactites_ids, stalagmites_ids]]) != 1:
            raise Exception("{} did not qualify a single time.".format(str(edge)))

    # Green
    for edge in sources:
        edge.origin.color = (0, 1, 0)
    # Teal
    for edge in sinks:
        edge.origin.color = (0, 1, 1)
    # Purple
    for edge in l_progress:
        edge.origin.color = (1, 0, 1)
    # Dusty yellow
    for edge in r_progress:
        edge.origin.color = (0.8, 0.8, 0)
    # Red
    for edge in stalagmites:
        edge.origin.color = (1, 0, 0)
    # Blue
    for edge in stalactites:
        edge.origin.color = (0, 0, 1)

    def monotonize_forward(face):
        # Categorize points (which are associated with half-edges)
        edges = face.border
        # Generate a BBST to hold the parts as they occur.
        # Use a data structure accessible from the outside to manage order checks.
        class X_Holder:
            def __init__(self):
                self.x = None
        x_holder = X_Holder()
        def cmp(a, b):
            a_left, a_helper, a_right = a
            b_left, b_helper, b_right = b
            x = x_holder.x
            if a_right.plot(x) < b_left.plot(x):
                return 1
            elif b_right.plot(x) < a_left.plot(x):
                return -1
            else:
                return 0
        t = RedBlackTree(cmp=cmp)
        d = {}
        print()
        # Process each event
        for edge in sorted(edges, key=lambda e: (e.origin.x, e.origin.y)):
            ex, ey = edge.origin.x, edge.origin.y
            x_holder.x = ex
            # Approach the point with the lowest yet-unhit x
            t.print_tree()
            # If a source is met, either generate a new BBST object
            if is_source(edge):
                # Set the side edges to a newly-generated trapezoid
                new_node = t.insert([edge.pred, edge, edge])
                d[id(edge.pred)] = d[id(edge.succ)] = new_node
            # If a sink is met, kill a BBST object
            elif is_sink(edge):
                print("Killing the sink at", ey, ex)
                # Delete the trapezoid from the data structure
                d[id(edge)].delete()
                d.pop(id(edge))
            # If left progress is met, move the left side of the appropriate BBST object
            elif is_l_progress(edge):
                print("Left!")
                if id(edge) not in d:
                    print("Could not find edge.")
                else:
                    # Find the trapezoid supported by incoming edge in the data structure
                    node = d[id(edge)]
                    left, helper, right = node.value
                    d.pop(id(left))
                    # Change the left edge to the successor of its current value
                    node.value = [edge.pred, edge, right]
                    # Set the helper to the newly-hit point
                    d[id(edge.pred)] = d[id(right.succ)] = node
            # If right progress is met, move the right side of the appropriate BBST object
            elif is_r_progress(edge):
                print("Right!")
                if id(edge) not in d:
                    print("Could not find edge.")
                else:
                    # Find the trapezoid supported by incoming edge in the data structure
                    node = d[id(edge)]
                    left, helper, right = node.value
                    d.pop(id(right.succ))
                    # Change the left edge to the successor of its current value
                    node.value = [left, edge, edge]
                    # Set the helper to the newly-hit point
                    d[id(left)] = d[id(edge.succ)] = node
            # If a stalagmite is met, split an existing trapezoid
            elif is_stalagmite(edge):
                # Pop the trapezoid at hand from the data structure
                node = t.head
                while node is not None and ey < node.value[0].plot(ex) or ey > node.value[2].plot(ex):
                    if ey < node.value[0].plot(ex):
                        node = node.left
                    elif ey > node.value[2].plot(ex):
                        node = node.right
                if node is None:
                    raise Exception("You have been unable to find where the given stalagmite rests.")
                left, helper, right = node.value
                node.delete()
                d.pop(id(left))
                d.pop(id(right.succ))
                node_left = t.insert([left, edge, edge])
                node_right = t.insert([edge.pred, edge, right])
                d[id(left)]      = d[id(edge.succ)]  = node_left
                d[id(edge.pred)] = d[id(right.succ)] = node_right
                print("FOUND IT!", str(left), str(right))
                # Generate two new half-edges in the graph so as to enclose the newly-generated subspace
                pr, rp = DCEL.HalfEdge.link_edges(helper, edge)
                pr.color = rp.color = (0, 0.5, 1)
                print("Newly-generated edges are", str(pr), str(rp))
            # If a stalactite is met, merge two trapezoids into one
            elif is_stalactite(edge):
                # Pop the trapezoid at hand from the data structure
                node = t.head
                while node is not None and ey < node.value[0].plot(ex) or ey > node.value[2].plot(ex):
                    if ey < node.value[0].plot(ex):
                        node = node.left
                    elif ey > node.value[2].plot(ex):
                        node = node.right
                if node is None:
                    raise Exception("You have been unable to find where the given stalactite rests.")
                elif str(node.value[0]) == str(edge):
                    left_side_node, right_side_node = node.left, node
                elif str(node.value[2].succ) == str(edge):
                    left_side_node, right_side_node = node, node.right
                else:
                    raise Exception("Your chosen side did not have a pairing match.")
                print("Stalactite at", str(edge.origin), str(edge))
                print("L:", [str(item) for item in left_side_node.value])
                print("R:", [str(item) for item in right_side_node.value])
                # Merge, but make no cut.
                # You can proceed along a reversed image of the polygon to generate cuts in the reverse direction.
                d.pop(id(right_side_node.value[0]))
                right_side_node.value = [left_side_node.value[0], edge, right_side_node.value[2]]
                print("F:", [str(item) for item in right_side_node.value])
                left_side_node.delete()
                d[id(right_side_node.value[0])] = d[id(right_side_node.value[2].succ)] = right_side_node
            # If a non-stalagmite non-stalagtite is met, simply move on.
            else:
                raise Exception("Invalid point & edge.", str(edge))
            print(str(edge.origin))
            for idn, node in d.items():
                print('\t', str(obj(idn).origin), [str(edge.origin) for edge in node.value])
            print('\n\n')
    # Monotonize one way
    monotonize_forward(inner_face)
    # Reallocate faces to reflect newly-generated sub-faces
    dcel.reallocate_faces()
    # Monotonize each sub-face the other way
    dcel.reflect()
    inner_faces = dcel.list_faces(include_outside=False)
    for face in inner_faces:
        monotonize_forward(face)
    dcel.reflect()
    # Reallocate face references
    dcel.reallocate_faces()


def monotone_x_triangulate(dcel):
    """
    Given the in-order points of a polygon monotone with respect to x,
    return a list of edges required to triangulate it.
    """
    print('\n\n\n\n')
    for face in dcel.list_faces():
        print('Border of current face:', list(map(lambda e: str(e.origin), face.border)))
        # Get a pointers to the start and end of this polygon, as well as pointers that we will use to track traversal
        rooted_edge = face.inc
        while not is_source(rooted_edge):
            rooted_edge = rooted_edge.succ
        # Generate linked list to act as a stack for unresolved points.
        q = deque([rooted_edge])

        # Define two triangulating functions
        def resolve_left():
            if len(q) >= 3 and is_ccw_turn(q[-1].origin.coord, q[-2].origin.coord, q[-3].origin.coord):
                print("Resolving left")
                while len(q) >= 3 and is_ccw_turn(q[-1].origin.coord, q[-2].origin.coord, q[-3].origin.coord):
                    # Remove the second-to-last point from the equation by forming a triangle with it as a point on the hull
                    a = q.pop()
                    q.pop()
                    c = q.pop()
                    print("Adding edge from", str(a.origin), "to", str(c.origin))
                    pr, rp = DCEL.HalfEdge.link_edges(a, c)
                    pr.color = rp.color = (1, 0.5, 1)
                    q.append(a)
                    q.append(rp)
                    print('\tQ is now', [str(e) for e in q])
                resolve_right()

        def resolve_right():
            if len(q) >= 3 and is_ccw_turn(q[2].origin.coord, q[1].origin.coord, q[0].origin.coord):
                print('Resolving right')
                while len(q) >= 3 and is_ccw_turn(q[2].origin.coord, q[1].origin.coord, q[0].origin.coord):
                    # Remove the second-to-last point from the equation by forming a triangle with it as a point on the hull
                    a = q.popleft()
                    q.popleft()
                    c = q.popleft()
                    print("Adding edge from", str(a.origin), "to", str(c.origin))
                    pr, rp = DCEL.HalfEdge.link_edges(a, c)
                    pr.color = rp.color = (1, 0.5, 0.5)
                    q.appendleft(pr)
                resolve_left()

        # While not at the end of both chains...
        i = 0
        done = False
        max_hit_count = len(face.border) + 5
        while i < max_hit_count and not done and (q[0].pred.origin.x > q[0].origin.x or q[-1].succ.origin.x > q[-1].origin.x):
            current_edges = dcel.generate_full_edge_list(including_outside=True)
            current_edge_ends = {(str(e.p0), str(e.p1)) for e in current_edges}
            for p0, p1 in current_edge_ends:
                if (p1, p0) not in current_edge_ends:
                    raise Exception('You have failed to match your edges.\n' + '\n'.join([str(item) for item in sorted(current_edge_ends)]))
            print(i, [str(e) for e in q])
            i += 1
            # Resolve both sides to move the pointers up the queue
            resolve_right()
            resolve_left()
            # print(is_sink(q[0].pred), is_sink(q[-1].succ), q[0].pred.origin.x, q[-1].succ.origin.x)
            if not is_sink(q[0].pred) and q[0].pred.origin.x <= q[-1].succ.origin.x:
                print('LQueueing', str(q[0].pred))
                q.appendleft(q[0].pred)
            elif not is_sink(q[-1].succ) and q[0].pred.origin.x > q[-1].succ.origin.x:
                print("RQueueing", str(q[-1].succ))
                q.append(q[-1].succ)
            else:
                print("Done is done!")
                done = True
        print(i, list(map(str, q)))
        print("Triangulated!")
        print('\n\n\n\n')
        if i == max_hit_count:
            raise Exception("Something has gone wrong with resolving this face.")
    # Reallocate faces to the new triangulation
    dcel.reallocate_faces()
    print("At the end of the day, the triangles are:")
    for face in dcel.list_faces():
        print("\t", str(face))
    print("DONE TRIANGULATING!")
    exit()
    # Return your final answer
    return []


def triangulate(dcel):
    """
    This function takes in a list of points, assumed to be the in-order points of a certain unholed polygon.
    This polygon input may not be convex, nor even necessarily monotone.
    The function partitions the inputs into monotone sections, then triangulates those now monotone sections.
    The final result is a list of segments that will successfully triangulate the input polygon.
    """
    generate_monotone_sections(dcel)
    for face in dcel.list_faces():
        print("BLARG: F:", [str(e) for e in face.border])
    for e in dcel.generate_full_edge_list(False):
        print("{:21}, {:21}, {:21}".format(str(e.pred), str(e), str(e.succ)))
    monotone_x_triangulate(dcel)


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


if __name__ == "__main__":
    test = "generated_example"
    test = "facial_debugger"
    if test == "bottom_spans_under_initial_indent_test_case":
        start = (91, 104)
        end = (119, 119)
        points = [
            (34, 49),
            (6, 35),
            (4, 30),
            (6, 25),
            (10, 8),
            (22, 19),
            (30, 20),
            (31, 28),
            (37, 10),
            (39, 20),
        ]
        points = [(y, 50 - x) for y, x in points]
        print(points)
    elif test == "facial_debugger":
        start = (91, 104)
        end = (119, 119)
        points = [
            (25, 20),
            (31, 28),
            (37, 10),
            (39, 20),
            (58, 33),
            (34, 49),
            (6, 42),
            (4, 32),
            (6, 25),
            (10, 8),
            (22, 19),
        ]
        points = [(y, 50 - x) for y, x in points]
        print(points)
    elif test == "oscillator":
        start = (91, 104)
        end = (119, 119)
        points = [
            (25, 25),
            (31, 28),
            (37, 10),
            (39, 20),
            (58, 33),
            (34, 49),
            (6, 42),
            (4, 32),
            (5, 25),
            (10, 8),
            (22, 19),
        ]
        points = [(y, 50 - x) for y, x in points]
        print(points)
    elif test == "generated_example":
        start = (91, 104)
        end = (119, 119)
        points = [
            (50, 39),
            (60, 45),
            (34, 49),
            (6, 35),
            (4, 30),
            (6, 25),
            (2, 20),
            (4, 15),
            (2, 10),
            (10, 8),
            (22, 24),
            (22, 19),
            (30, 20),
            (31, 28),
            (37, 10),
            (39, 20),
            (58, 33),
        ]
        points = [(y, 50 - x) for y, x in points]
        print(points)
    elif test == "stalagmite_test_case":
        start = (91, 104)
        end = (119, 119)
        points = [
            (34, 5),
            (6, 15),
            (10, 42),
            (25, 25),
            (37, 40),
            (58, 17),
        ]
        print(points)
    elif test == "stalagmite_stalactite_test_case":
        start = (91, 104)
        end = (119, 119)
        points = [
            (34, 49),
            (6, 38),
            (20, 20),
            (25, 30),
            (30, 20),
            (31, 28),
            (37, 10),
            (39, 29),
        ]
    elif test == "stalagmite_stalactite_test_case_2":
        start = (91, 104)
        end = (119, 119)
        points = [
            (104, 129),
            (76, 118),
            (90, 100),
            (95, 110),
            (92, 99),
            (100, 100),
            (101, 108),
            (107, 90),
            (109, 109),
            (128, 113),
        ]
        points = [(y - 70, x - 80) for y, x in points]
    elif test == "actual_example":
        start = (91, 104)
        end = (119, 119)
        points = [
            (104, 129),
            (76, 118),
            (90, 100),
            (95, 110),
            (92, 99),
            (100, 100),
            (101, 108),
            (107, 90),
            (109, 109),
            (128, 113),
        ]
        points = [(y - 70, x - 80) for y, x in points]
    elif test == "basic_triangle_1":
        start = (1, 2)
        end = (2, 3)
        points = [
            (0, 0),
            (0, 2),
            (4, 2),
        ]
    elif test == "basic_triangle_2":
        start = (1, 2)
        end = (2, 3)
        points = [
            (0, 0),
            (1, 2),
            (4, 2),
        ]
    elif test == "basic_triangle_3":
        start = (1, 2)
        end = (2, 3)
        points = [
            (1, 0),
            (0, 2),
            (4, 2),
        ]
    else:
        raise Exception("Improper test case!")
    # Generate a blank polygon, correctly oriented
    dcel = DCEL(points)
    # Triangulate said polygon
    triangulate(dcel)
    # Get an edge list from the polygon
    edge_list = dcel.generate_full_edge_list(including_outside=False)
    # Adjust the DCEL parameters to correctly display the chosen item
    DCEL.line_side_offset = 5
    DCEL.end_shortening = 20
    DCEL.wh_pixels = 800
    DCEL.adj = 20
    DCEL.wh_n = max([y for y, x in points] + [x for y, x in points]) * 1.1
    print("WHN IS ", DCEL.wh_n)
    DCEL.readjust()
    # Label faces as convex or not
    ids1 = set(map(id, dcel.list_faces()))
    ids2 = set(map(id, dcel.list_faces()))
    dif12 = sorted(list(ids1.difference(ids2)))
    print("{} items:\n\t".format(len(dif12)), '\n\t '.join([str(n) for n in dif12]))
    dif21 = sorted(list(ids2.difference(ids1)))
    print("{} items:\n\t".format(len(dif21)), '\n\t '.join([str(n) for n in dif21]))
    same12 = sorted([n for n in ids1 | ids2 if n not in dif12 and n not in dif21])
    print("{} items:\n\t".format(len(same12)), '\n\t '.join(sorted([str(obj(n)) for n in same12])))
    print("HELLO")
    # print(len(faces))
    # for face in faces:
    #     face.color = (1, 0, 1)
    #     print(face.color)
    # for face in faces:
    #     print(face.color)
    # Draw the completed result
    def draw():
        dcel.draw()
    start_graphics(draw, width=DCEL.wh_pixels, height=DCEL.wh_pixels)
