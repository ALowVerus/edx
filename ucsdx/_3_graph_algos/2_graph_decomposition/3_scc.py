# Uses python3

import sys

sys.setrecursionlimit(200000)


def pprint(*args):
    if False:
        print(*args)


def find_strongly_connected_components(adj):
    """
    Given an adjacency list, find all strongly-connected components and return them.
    """
    pprint('adj:', adj)
    # Use DFS to assign a numbering to all vertices
    hit_queue = []
    vertex_q = list(range(len(adj)))
    ordering = []
    seen = set()
    while vertex_q:
        # Grab a root vertex
        root_vertex = vertex_q.pop()
        # If the root vertex has yet to be seen, it is a valid place to root a component
        if root_vertex not in seen:
            # Note that the root has been seen
            seen.add(root_vertex)
            hit_queue.append([root_vertex, 0])
            # So long as there are paths to traverse, traverse them
            while hit_queue:
                pprint('    ', hit_queue)
                if hit_queue[-1][1] < len(adj[hit_queue[-1][0]]):
                    next_v = None
                    if adj[hit_queue[-1][0]][hit_queue[-1][1]] not in seen:
                        next_v = adj[hit_queue[-1][0]][hit_queue[-1][1]]
                    # Regardless of whether something is added to the stack, progress onward
                    hit_queue[-1][1] += 1
                    # If the next target is valid, add it to the q
                    if next_v is not None:
                        seen.add(next_v)
                        hit_queue.append([next_v, 0])
                else:
                    ordering.append(hit_queue.pop()[0])
    pprint(',')
    pprint('Ordering:', ordering)
    # Generate a reversed adjacency list
    adj_reversed = [[] for i in adj]
    for i, targets in enumerate(adj):
        for t in targets:
            adj_reversed[t].append(i)
    pprint('adj_r:', adj_reversed)
    # Using a reversed DFS, grab strongly connected components
    components = []
    seen = set()
    while ordering:
        root_vertex = ordering.pop()
        if root_vertex not in seen:
            component = set()
            seen.add(root_vertex)
            hit_queue = [[root_vertex, 0]]
            while hit_queue:
                if hit_queue[-1][1] < len(adj_reversed[hit_queue[-1][0]]):
                    next_v = None
                    if adj_reversed[hit_queue[-1][0]][hit_queue[-1][1]] not in seen:
                        next_v = adj_reversed[hit_queue[-1][0]][hit_queue[-1][1]]
                    # Regardless of whether something is added to the stack, progress onward
                    hit_queue[-1][1] += 1
                    if next_v is not None:
                        seen.add(next_v)
                        hit_queue.append([next_v, 0])
                else:
                    component.add(hit_queue.pop()[0])
            components.append(component)
    pprint('Components:', components)
    pprint(',')
    return components


def number_of_strongly_connected_components(adj):
    # write your code here
    return len(find_strongly_connected_components(adj))


if __name__ == '__main__':
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n, m = data[0:2]
    data = data[2:]
    edges = list(zip(data[0:(2 * m):2], data[1:(2 * m):2]))
    adj = [[] for _ in range(n)]
    for (a, b) in edges:
        adj[a - 1].append(b - 1)
    print(number_of_strongly_connected_components(adj))
