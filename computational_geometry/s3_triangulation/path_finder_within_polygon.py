from computational_geometry.dcel import DCEL
from computational_geometry.s3_triangulation.triangulator import triangulate
from computational_geometry.drawing_lib import *
from collections import deque


def generate_triangle_path_from_start_to_end(dcel, start, end):
    # Seat the start and end within triangles
    faces = dcel.list_faces()
    try:
        f_s = [f for f in faces if f.contains_vertex(start)][0]
    except Exception:
        raise Exception("You have been unable to place the start vertex within the DCEL.")
    try:
        f_e = [f for f in faces if f.contains_vertex(end)][0]
    except Exception:
        raise Exception("You have been unable to place the end vertex within the DCEL.")
    # BFS path from start to end through the DCEL
    back_pointers = {id(f_s): [None, None]}
    q = deque([f_s])
    while q[0] != f_e:
        item = q.popleft()
        for e in item.border:
            if id(e.twin.face) not in back_pointers and e.twin.face is not dcel.outer:
                back_pointers[id(e.twin.face)] = [id(item), e]
                q.append(e.twin.face)
    path = [back_pointers[id(f_e)][1]]
    while path[-1].face is not f_s:
        path.append(back_pointers[id(path[-1].face)][1])
    path = path[::-1]
    for e in path:
        e.color = (1, 1, 0)
    # If f_s is f_e, return a simple path inside the triangle
    if f_s is f_e:
        sub_dcel = DCEL()
        ab, ba = DCEL.generate_half_edge_pair(start, end)
        ab.face = ba.face = dcel.outer
        sub_dcel.outer.inc = ab
    # If there are possible kinks, resolve the shortest path
    else:
        # First, create a simplified dual graph
        hashed_mirror_points = {}
        for e in path:
            for v in [e.origin, e.twin.origin]:
                if v.coord not in hashed_mirror_points:
                    hashed_mirror_points[v.true_coord] = DCEL.Vertex(v.true_coord)
        hashed_mirror_points[start.true_coord] = start
        hashed_mirror_points[end.true_coord] = end
        sub_dcel = DCEL()
        # Seed with a face for the first 3 points
        first_face = DCEL.Face()
        a, b, c = [hashed_mirror_points[v.true_coord] for v in [start, path[0].origin, path[0].twin.origin]]
        ab, ba = DCEL.generate_half_edge_pair(a, b)
        bc, cb = DCEL.generate_half_edge_pair(b, c)
        ca, ac = DCEL.generate_half_edge_pair(c, a)
        ab.face = bc.face = ca.face = first_face
        ba.face = cb.face = ac.face = sub_dcel.outer
        sub_dcel.outer.inc = ba
        first_face.inc = ab
        ab.succ = ca.pred = bc
        bc.succ = ab.pred = ca
        ca.succ = bc.pred = ab
        ba.succ = cb.pred = ac
        cb.succ = ac.pred = ba
        ac.succ = ba.pred = cb
        # Iteratively expand outward toward the remaining faces
        curr_face = first_face
        for path_e in path[:]:
            matching_edge = [curr_e for curr_e in curr_face.border if str(curr_e) == str(path_e)][0]
            if path_e != path[-1]:
                newly_added_v = [v for v in path_e.twin.face.vertices
                                 if str(v) != str(path_e.origin) and str(v) != str(path_e.twin.origin)][0]
                newly_added_v = hashed_mirror_points[newly_added_v.true_coord]
            else:
                newly_added_v = hashed_mirror_points[end.true_coord]
            new_face = DCEL.Face()
            new_face.inc = matching_edge.twin
            ab, ba = matching_edge.twin, matching_edge
            a, b, c = ab.origin, ba.origin, newly_added_v
            bc, cb = DCEL.generate_half_edge_pair(b, c)
            ca, ac = DCEL.generate_half_edge_pair(c, a)
            ab.face = bc.face = ca.face = new_face
            cb.face = ac.face = sub_dcel.outer
            ac.succ = cb
            cb.pred = ac
            ac.pred = ab.pred
            ac.pred.succ = ac
            cb.succ = ab.succ
            cb.succ.pred = cb
            ab.succ = ca.pred = bc
            bc.succ = ab.pred = ca
            ca.succ = bc.pred = ab
            a.inc = ab
            b.inc = bc
            c.inc = ca
            curr_face = new_face
    # Recolor all faces yellow for easy viewing
    for f in sub_dcel.list_faces():
        f.color = (1, 1, 0)
    return sub_dcel


def convert_triangle_path_to_event_queue(sub_dcel, start, end):
    curr_edge = start.inc.twin.pred
    q = [(start, "L"), (start, "R"), (curr_edge.origin, 'R'), (curr_edge.twin.origin, 'L')]
    done = False
    while not done:
        if curr_edge.twin.pred.origin is end:
            done = True
        # On right transition, add a right transition to the q
        elif curr_edge.twin.succ.twin.face is not sub_dcel.outer:
            curr_edge = curr_edge.twin.succ
            q.append([curr_edge.succ.origin, 'L'])
        # On left transition, add a left transition to the q
        elif curr_edge.twin.pred.twin.face is not sub_dcel.outer:
            curr_edge = curr_edge.twin.pred
            q.append([curr_edge.origin, 'R'])
        # If neither left nor right transition applies, you've screwed up
        else:
            raise Exception("Ya dun goofed.")
    q.extend([(end, 'L'), (end, 'R')])
    return q


def find_path_within_polygon(dcel, start, end):
    # Generate a simplified path of triangles from start to end
    sub_dcel = generate_triangle_path_from_start_to_end(dcel, start, end)
    # Now that a simplified search space exists, convert it into a queue of events expanding a given partial path
    q = convert_triangle_path_to_event_queue(sub_dcel, start, end)
    print("A queue has been populated with a series of new triangle events to process.")
    print("Q:", [[str(v), d] for v, d in q])
    # From the simplified queue, generate a path from start to end
    p = []
    s_l = deque()
    s_r = deque()
    for v, d in q:
        # Process the new event
        print(str(v), d)
        if d == 'R':
            s_r.append(v)
            # Check for inward bending
            while len(s_r) >= 2 and len(s_l) >= 2 and DCEL.is_ccw_turn(s_l[0], s_l[1], s_r[-1]):
                p.append(s_l.popleft())
                s_r.popleft()
                s_r.appendleft(s_l[0])
                print("INWARD BEND!")
            # Check for outward expansion
            while len(s_r) >= 3 and DCEL.is_ccw_turn(s_r[-3], s_r[-2], s_r[-1]):
                item_n1 = s_r.pop()
                s_r.pop()
                s_r.append(item_n1)
        elif d == 'L':
            s_l.append(v)
            # Check for inward bending
            while len(s_l) >= 2 and len(s_r) >= 2 and DCEL.is_ccw_turn(s_l[-1], s_r[1], s_r[0]):
                p.append(s_r.popleft())
                s_l.popleft()
                s_l.appendleft(s_r[0])
                print("INWARD BEND!")
            # Check for outward expansion
            while len(s_l) >= 3 and DCEL.is_ccw_turn(s_l[-1], s_l[-2], s_l[-3]):
                item_n1 = s_l.pop()
                s_l.pop()
                s_l.append(item_n1)
        else:
            raise Exception()
        # Resolve any new consisted path points
        while len(s_l) >= 2 and len(s_r) >= 2 and s_l[0] == s_r[0] and s_l[1] == s_r[1]:
            p.append(s_l.popleft())
            s_r.popleft()
        # Print results
        print("P:", [str(v) for v in p])
        print("L:", [str(v) for v in s_l])
        print("R:", [str(v) for v in s_r])
    p.append(end)
    # Convert the path into a dcel
    path_dcel = DCEL()
    p = [DCEL.Vertex(v.true_coord) for v in p]
    for v in p:
        v.color = (1, 0, 0)
    edges = [DCEL.generate_half_edge_pair(p[i + 0], p[i + 1]) for i in range(len(p) - 1)]
    for i in range(len(edges) - 1):
        ((ab, ba), (bc, cb)) = (edges[i + 0], edges[i + 1])
        ab.succ = bc
        bc.pred = ab
        cb.succ = ba
        ba.pred = cb
    for ab, ba in edges:
        ab.face = ba.face = path_dcel.outer
        ab.color = ba.color = (1, 0, 0)
    path_dcel.outer.inc = p[0].inc
    path_dcel.outer.inc.color = (1, 1, 1)
    return path_dcel


if __name__ == "__main__":
    test = "multiple_inversions"
    if test == "actual_example":
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
        start, end = [(y - 70, x - 80) for y, x in [start, end]]
    elif test == "oscillator":
        start = (10, 20)
        end = (37, 20)
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
    elif test == "multiple_inversions":
        start = (10, 220)
        end = (237, 245)
        points = [
            (19, 97),
            (0, 193),
            (5, 258),
            (37, 268),
            (29, 200),
            (35, 131),
            (53, 114),
            (54, 228),
            (56, 268),
            (87, 261),
            (90, 207),
            (79, 107),
            (72, 44),
            (130, 50),
            (105, 98),
            (142, 202),
            (111, 270),
            (172, 248),
            (198, 176),
            (239, 230),
            (160, 283),
            (237, 287),
            (294, 221),
            (232, 128),
            (163, 165),
            (142, 119),
            (267, 94),
            (257, 59),
            (310, 117),
            (284, 163),
            (311, 192),
            (351, 81),
            (249, 9),
            (218, 60),
            (143, 82),
            (165, 18),
            (66, 0),
        ]
    else:
        raise Exception()
    # Generate a DCEL
    dcel = DCEL(points)
    # Triangulate it
    triangulate(dcel)
    print("Polygon has been triangulated.")

    # Get an edge list from the polygon
    edge_list = dcel.generate_full_edge_list(including_outside=False)
    # Recolor the points of the polygon
    for v in dcel.list_vertices():
        v.color = (0, 0.7, 0)

    # Pointify the points
    start = DCEL.Vertex(start)
    end = DCEL.Vertex(end)
    start.color = end.color = (1, 0, 0)

    # Generate a path from start to end within the polygon
    path_dcel = find_path_within_polygon(dcel, start, end)

    # Calculate the path length
    segs = [[e.origin, e.succ.origin] for e in path_dcel.generate_full_edge_list(including_outside=True)]
    path_length = sum([((a.y - b.y) ** 2 + (a.x - b.x) ** 2) ** 0.5 for a, b in segs]) / 2
    print("Path length is", path_length)

    # Adjust the DCEL parameters to correctly display the chosen item
    DCEL.line_side_offset = 5
    DCEL.end_shortening = 20
    DCEL.wh_pixels = 800
    DCEL.adj = 20
    DCEL.wh_n = max([y for y, x in points] + [x for y, x in points]) * 1.1
    print("WHN IS ", DCEL.wh_n)
    DCEL.readjust()

    def draw():
        dcel.draw()
        path_dcel.draw()

    start_graphics(draw, width=DCEL.wh_pixels, height=DCEL.wh_pixels)
