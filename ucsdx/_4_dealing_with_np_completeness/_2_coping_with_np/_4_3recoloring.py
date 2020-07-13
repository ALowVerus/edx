# python3
def assign_new_colors_actor(adjacencies, initial_colorings):
    def sat_2(clauses):
        def neg(var):
            return var[1:] if var[0] == '-' else '-' + var

        """
        Given a set of 2-SAT clauses, determine whether a valid solution exists.
        """
        variables = set()
        for clause in clauses:
            for term in clause:
                variables.add(term.replace('-', ''))
        variables = list(variables)
        # Generate vertices for each variable and its negation
        vertices = {}
        for v in variables:
            vertices[v] = set()
            vertices[neg(v)] = set()
        # Load the vertex edges with clauses, use sets to prevent dupes
        for clause in clauses:
            if len(clause) == 1:
                a = clause[0]
                vertices[neg(a)].add(a)
            elif len(clause) == 2:
                a, b = clause
                vertices[neg(a)].add(b)
                vertices[neg(b)].add(a)
            else:
                raise Exception('Clause does not have 1 or 2 arguments.')
        # Convert to using lists as values to allow indexing
        vertices = {v: list(t) for v, t in vertices.items()}

        # Divide the vertices into strongly connected components
        def find_strongly_connected_components(adj):
            """
            Given an adjacency list, find all strongly-connected components and return them.
            """
            # Use DFS to assign a numbering to all vertices
            hit_queue = []
            vertex_q = set(adj.keys())
            ordering = []
            seen = set()
            while vertex_q:
                # Grab a root vertex
                root_vertex = vertex_q.pop()
                # If the root vertex has yet to be seen, it is a valid place to root a component
                if root_vertex not in seen:
                    # Note thate the root has been seen
                    seen.add(root_vertex)
                    hit_queue.append([root_vertex, 0])
                    # So long as there are paths to traverse, traverse them
                    while hit_queue:
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
            # Generate a reversed adjacency list
            adj_reversed = {}
            for source, targets in vertices.items():
                if source not in adj_reversed:
                    adj_reversed[source] = set()
                for target in targets:
                    if target not in adj_reversed:
                        adj_reversed[target] = set()
                    adj_reversed[target].add(source)
            adj_reversed = {source: list(targets) for source, targets in adj_reversed.items()}
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
            return components

        components = find_strongly_connected_components(vertices)[::-1]
        # Check whether any strongly connected component links a variable to its negation
        for component in components:
            for item in component:
                if item in component and neg(item) in component:
                    return None
        # Otherwise, give 1s to all connected items. If the item is a negative, give 0.
        variable_assignments = {}
        for component in components:
            for item in component:
                if item in variable_assignments or neg(item) in variable_assignments:
                    pass
                elif '-' in item:
                    variable_assignments[neg(item)] = 0
                else:
                    variable_assignments[item] = 1
        # Return the result.
        res = [('' if r else '-') + var for var, r in variable_assignments.items()]
        return res

    boolean_checks = set()
    for i, initial_color in initial_colorings.items():
        boolean_checks.add('-{}_{}'.format(i, initial_color))
        boolean_checks.add(' '.join(
            ['{}_{}'.format(i, possible_color) for possible_color in [c for c in "RGB" if c != initial_color]]))
    for p0, neighbors in adjacencies.items():
        for p1 in neighbors:
            c0, c1 = sorted((p0, p1))
            for color in "RGB":
                check = "-{}_{} -{}_{}".format(c0, color, c1, color)
                boolean_checks.add(check)
    for i in range(len(adjacencies)):
        for color in "RGB":
            boolean_checks.add("{}_{} -{}_{}".format(i, color, i, color))
    boolean_checks = sorted(boolean_checks)
    boolean_checks = [check.split(' ') for check in boolean_checks]
    res = sat_2(boolean_checks)
    if res is None:
        return None
    new_colorings = [val.split('_') for val in res if '-' not in val]
    new_colorings = {int(i): color for i, color in new_colorings}
    return new_colorings


# Arguments:
#   * `n` - the number of vertices.
#   * `edges` - list of edges, each edge is a tuple (u, v), 1 <= u, v <= n.
#   * `colors` - list consisting of `n` characters, each belonging to the set {'R', 'G', 'B'}.
# Return value:
#   * If there exists a proper recoloring, return value is a list containing new colors, similar to the `colors` argument.
#   * Otherwise, return value is None.
def assign_new_colors(n, edges, colors):
    colorings = {i: colors[i-1] for i in range(1, n+1)}
    adj = {i: set() for i in range(1, n+1)}
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    res = assign_new_colors_actor(adj, colorings)
    if res is None:
        return None
    else:
        return [res[i] for i in range(1, n+1)]


def main():
    if True:
        n, m = map(int, input().split())
        colors = input()
        edges = []
        for i in range(m):
            u, v = map(int, input().split())
            edges.append((u, v))
    else:
        lines = """
        4 5
        RRRG
        1 3
        1 4
        3 4
        2 4
        2 3
        """.split('\n')[1:-1]
        n, m = map(int, lines[0].split())
        colors = lines[1].strip()
        edges = [map(int, line.split()) for line in lines[2:]]

    new_colors = assign_new_colors(n, edges, colors)
    if new_colors is None:
        print("Impossible")
    else:
        print(''.join(new_colors))


main()
