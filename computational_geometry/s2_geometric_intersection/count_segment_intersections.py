from computational_geometry.s2_geometric_intersection.red_black_segment_tree import *
from computational_geometry.s2_geometric_intersection.segment_event_heap import *


def brute_solve(segments):
    intersections = []
    for i in range(len(segments)):
        for j in range(i+1, len(segments)):
            new_intersections = check_intersection(segments[i], segments[j])
            intersections.extend(new_intersections)
    print()
    print("Final intersections:")
    for intersection in intersections:
        print('\t', intersection)
    return intersections


def sweepline_solve(segments):
    # Separate vertical lines from others, since they will break the x-based comparisons
    verticals = [seg for seg in segments if seg[0][0] == seg[1][0]]
    verticals_dict = {}
    for seg in verticals:
        if seg[0][0] not in verticals_dict:
            verticals_dict[seg[0][0]] = []
        verticals_dict[seg[0][0]].append(seg)
    # Use non-vertical lines as valid entry points in the sweepline
    segments = [seg for seg in segments if seg[0][0] != seg[1][0]]
    # Get a queue for the start and end points of the lines, which will have to be dealt with eventually regardless
    po_to_line = {}
    pf_to_line = {}
    for po, pf in segments:
        if po not in po_to_line:
            po_to_line[po] = []
        po_to_line[po].append((po, pf))
        if pf not in pf_to_line:
            pf_to_line[pf] = []
        pf_to_line[pf].append((po, pf))

    # Initialize a queue to hold the actions as they come in
    h = SegmentEventHeap()

    # Load the heap up with the start and end points. Hash them first to remove dupes.
    for p in {p for p in list(po_to_line.keys()) + list(pf_to_line.keys())}:
        h.add('Point', p)

    # Load the heap up with the x-coordinates of the verticals
    for x in verticals_dict:
        h.add('Vertical', x)

    # Initialize a structure to hold the currently-valid line segments
    t = RedBlackSegmentTree()

    print(sorted(list(po_to_line.keys())))
    print(sorted(list(pf_to_line.keys())))
    print(sorted(list(verticals_dict.keys())))

    # While there are events in the queue, keep popping!
    intersections = []
    while len(h.entries) > 0:
        print()
        curr_x = h.entries[0][0]
        print("Intersections already hit are:")
        for item in intersections:
            print("    ", item)
        print("Popping at x={}".format(curr_x))
        t.print_tree()
        t.print_list()
        # Pop an item from the heap
        points_on_x, hits_vertical = h.step()
        print(points_on_x, hits_vertical)
        # Add all the new lines with start points at this x to the RBTree
        for po in points_on_x:
            if po in po_to_line:
                for segment in po_to_line[po]:
                    print("Adding new segment to the size {} tree: {}".format(t.size, segment))
                    new_intersection_points = t.insert(segment, curr_x)
                    print("Size is now {}.".format(t.size))
                    for p in new_intersection_points:
                        print("Generated new intersection point", p)
                        if p[0] > curr_x + LEEWAY:
                            h.add('Point', p)
                # Pop to prevent double adds of any given segments
                po_to_line.pop(po)
        print()
        print("After adding points for this round:")
        t.print_tree()
        t.print_list()
        print("Size is", t.size)
        # If there are verticals to deal with...
        if curr_x in verticals_dict:
            # Check lines currently in the RBTree against the vertical hits to find crossings
            if t.size > 0:
                # For each vertical
                for vertical in verticals_dict[curr_x]:
                    # Find the point closest to the target
                    match = t.find_nearest(vertical[0])
                    while match.std_form is not None and match.plot(x) >= vertical[0][1]:
                        match = match.prev
                    # Overshot, move up one
                    match = match.next
                    # Iterate downwards, increasing y, until going OOB, adding hit segments to the list of segments
                    lines_between = []
                    while match.std_form is not None and match.plot(x) <= vertical[1][1]:
                        lines_between.append(match)
                        match = match.next
                    # Generate intersection objects
                    for line in lines_between:
                        for segment in line.segments:
                            intersections.append([segment, vertical, [[curr_x, line.plot(curr_x)]]])
            # Scan the verticals against each other to get segment overlaps
            vertical_segments = sorted(verticals_dict[curr_x])
            for i in range(len(vertical_segments)):
                j = i+1
                while j < len(vertical_segments) and vertical_segments[i][1][1] >= vertical_segments[j][0][1]:
                    intersection = check_intersection(vertical_segments[i], vertical_segments[j])
                    if intersection:
                        intersections.append((vertical_segments[i], vertical_segments[j], intersection))
                    j += 1
        # Deal with any intersections at this x
        # If there are items inside the line structure, check for intersections
        if t.size > 0:
            for pi in points_on_x:
                # Get to the neighborhood of the intersection
                curr_intersecting_line = t.find_nearest(pi)
                print('Intersecting line nearest to {}: {}'.format(pi, curr_intersecting_line.segments))
                # Get to the top line
                while curr_intersecting_line.std_form is not None and curr_intersecting_line.plot(pi[0]) >= pi[1] - LEEWAY:
                    curr_intersecting_line = curr_intersecting_line.prev
                curr_intersecting_line = curr_intersecting_line.next
                print('Lowest Intersecting line hitting {}: {}'.format(pi, curr_intersecting_line.segments))
                # Move down until all crossing lines are enumerated
                crossing_lines = []
                while curr_intersecting_line.std_form is not None and curr_intersecting_line.plot(pi[0]) <= pi[1] + LEEWAY:
                    crossing_lines.append(curr_intersecting_line)
                    curr_intersecting_line = curr_intersecting_line.next
                # Remove invalid lines. The fact that this is required implies that the previous checks are not valid.
                crossing_lines = [line for line in crossing_lines if pi[1] - LEEWAY < line.plot(pi[0]) < pi[1] + LEEWAY]
                print('Crossing lines at {}: {}'.format(pi, [line.segments for line in crossing_lines]))
                # Reverse order of the crossing lines
                if len(crossing_lines) >= 2:
                    print("An intersection has occurred.", pi)
                    # Reverse the intersecting lines - after crossing a single point, they should essentially be reversed.
                    for i in range(len(crossing_lines)//2):
                        RedBlackSegmentTree.RedBlackNode.swap_node_connections(crossing_lines[i], crossing_lines[len(crossing_lines)-i-1])
                    crossing_lines = crossing_lines[::-1]
                    # Add the new front and back intersection points to the heap.
                    if crossing_lines[0].prev.std_form is not None:
                        bot_intersection_hits = check_intersection(crossing_lines[0].prev.segments[0], crossing_lines[0].segments[0])
                        if len(bot_intersection_hits) == 1:
                            bot_intersection_coords = bot_intersection_hits[0][2]
                            if len(bot_intersection_coords) == 1:
                                bot_intersection_point = bot_intersection_coords[0]
                                if bot_intersection_point[0] > curr_x + LEEWAY:
                                    h.add("Point", bot_intersection_point)
                    if crossing_lines[-1].next.std_form is not None:
                        top_intersection_hits = check_intersection(crossing_lines[-1].segments[0], crossing_lines[-1].next.segments[0])
                        if len(top_intersection_hits) == 1:
                            top_intersection_coords = top_intersection_hits[0][2]
                            if len(top_intersection_coords) == 1:
                                top_intersection_point = top_intersection_coords[0]
                                if top_intersection_point[0] > curr_x + LEEWAY:
                                    h.add("Point", top_intersection_point)
                    # Add intersections for all lines in the crossing section, in O(n^2) time
                    for i in range(len(crossing_lines)):
                        for segment_i in crossing_lines[i].segments:
                            for j in range(i+1, len(crossing_lines)):
                                for segment_j in crossing_lines[j].segments:
                                    intersections.append((segment_i, segment_j, (pi,)))
        print("After resolving intersections:")
        t.print_tree()
        t.print_list()
        print()
        # Remove all old lines with end points at this x from the RBTree
        for pf in points_on_x:
            if pf in pf_to_line:
                for segment in pf_to_line[pf]:
                    new_intersection_points = t.delete(segment, curr_x)
                    print(new_intersection_points)
                    for p in [item[2][0] for item in new_intersection_points]:
                        if p[0] > curr_x + LEEWAY:
                            h.add('Point', p)
                # Pop to prevent intersections from double counting
                pf_to_line.pop(pf)
        print(len(intersections))
        print()
        print()
        print()
    # Once the event heap is empty, return the result
    print(t.size)
    print('Final intersections:', intersections)
    return intersections


if __name__ == "__main__":
    from random import randint

    print()
    # Generate segments
    segs = generate_line_segments(8, 10)
    # segs = [((5, 1), (8, 1)), ((3, 9), (4, 4)), ((2, 9), (6, 2))]
    # segs = [((1, 6), (5, 3)), ((3, 4), (5, 7)), ((5, 1), (10, 3))][:3]
    # segs = [((10, 1), (10, 3)), ((0, 4), (6, 3)), ((1, 7), (1, 8))]
    # segs = [((0, 4), (1, 3)), ((1, 3), (10, 1)), ((7, 1), (8, 2))]
    # segs = [((1, 4), (4, 9)), ((2, 8), (8, 7)), ((0, 6), (10, 10))]
    # segs = [((1, 1), (7, 2)), ((3, 1), (6, 2)), ((5, 5), (8, 3))]
    # segs = [((0, 2), (4, 10)), ((1, 4), (10, 10)), ((2, 6), (7, 2))]
    # segs = [((3, 10), (9, 7)), ((4, 0), (10, 6)), ((3, 6), (10, 5)), ((9, 0), (9, 3)), ((7, 9), (9, 10)), ((8, 0), (8, 7)), ((8, 10), (10, 2)), ((3, 10), (7, 8))]
    segs = [((3, 4), (8, 4)), ((0, 7), (6, 7)), ((1, 4), (8, 10)), ((2, 7), (8, 0)), ((2, 5), (10, 9)), ((1, 8), (10, 7)), ((1, 8), (5, 7))]
    print(segs)
    print()
    # Compare various implementations of the intersection solving problem
    method_counts = {}
    for name, solve in [("Brute", brute_solve), ("Sweep", sweepline_solve)][:2]:
        print("Testing {}.".format(name))
        res = solve(segs)
        # for l1, l2, hit in res:
        #     print('L1: {}; L2: {}; Hit: {}'.format(l1, l2, hit))
        print("Total intersections:", len(res))
        print()
        method_counts[name] = len(res)
    print()
    print(method_counts)

    from cs1lib import *

    def draw():
        clear()
        set_stroke_color(0.1, 0.1, 0.1)
        set_stroke_width(1)
        for n in range(20):
            a, b, c, d = 0, n, 200, n
            a, b, c, d = [n * 30 for n in (a, b, c, d)]
            draw_line(a, b, c, d)
            a, b, c, d = n, 0, n, 200
            a, b, c, d = [n * 30 for n in (a, b, c, d)]
            draw_line(a, b, c, d)
        set_stroke_color(0, 0, 0)
        set_stroke_width(3)
        for ((a, b), (c, d)) in segs:
            a, b, c, d = [n * 30 for n in (a, b, c, d)]
            draw_line(a, b, c, d)
    start_graphics(draw)
