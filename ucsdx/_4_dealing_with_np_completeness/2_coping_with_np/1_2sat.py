# python3
def is_satisfiable(clauses):
    def pprint(*args):
        if False:
            print(*args)
    """
    Given a set of 2-SAT clauses, determine whether a valid solution exists.
    """
    # Convert all input variables into straight integers
    variables = set()
    for clause in clauses:
        for term in clause:
            variables.add(term.replace('-', ''))
    vars_to_nums = {}
    for i, v in enumerate(variables):
        vars_to_nums[v] = i+1
    nums_to_vars = {}
    for v, i in vars_to_nums.items():
        nums_to_vars[i] = v
    for clause in clauses:
        for i in range(len(clause)):
            clause[i] = (-1 if '-' in clause[i] else 1) * vars_to_nums[clause[i].replace('-', '')]
    # Generate vertices for each variable and its negation
    vertices = {}
    for n in nums_to_vars:
        vertices[n] = set()
        vertices[-n] = set()
    # Load the vertex edges with clauses, use sets to prevent dupes
    for clause in clauses:
        if len(clause) == 1:
            a = clause[0]
            vertices[-a].add(a)
        elif len(clause) == 2:
            a, b = clause
            vertices[-a].add(b)
            vertices[-b].add(a)
        else:
            raise Exception('Clause does not have 1 or 2 arguments.')
    # Convert to using lists as values to allow indexing
    vertices = {v: list(t) for v, t in vertices.items()}
    # Divide the vertices into strongly connected components
    def find_strongly_connected_components(adj):
        """
        Given an adjacency list, find all strongly-connected components and return them.
        """
        pprint('adj:', adj)
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
        adj_reversed = {}
        for source, targets in vertices.items():
            if source not in adj_reversed:
                adj_reversed[source] = set()
            for target in targets:
                if target not in adj_reversed:
                    adj_reversed[target] = set()
                adj_reversed[target].add(source)
        adj_reversed = {source: list(targets) for source, targets in adj_reversed.items()}
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
    components = find_strongly_connected_components(vertices)[::-1]
    pprint('Components:')
    pprint([{('' if var > 0 else '-') + str(nums_to_vars[abs(var)]) for var in component} for component in components])
    # Check whether any strongly connected component links a variable to its negation
    for component in components:
        for item in component:
            if item in component and -item in component:
                pprint('No valid results possible.')
                return None
    # Otherwise, give 1s to all connected items. If the item is a negative, give 0.
    variable_assignments = {}
    for component in components:
        for item in component:
            if item in variable_assignments or -item in variable_assignments:
                pass
            elif item < 0:
                variable_assignments[-item] = 0
            else:
                variable_assignments[item] = 1
    # Convert variables back into their initial forms
    res = sorted([('' if r else '-') + str(nums_to_vars[var]) for var, r in variable_assignments.items()],
                 key=lambda v: '{:>6}'.format(v.replace('-', '')))
    pprint('One valid result:')
    return res


if True:
    n, m = map(int, input().split())
    clauses = [list(input().split()) for i in range(m)]
else:
    clauses = [
        ["-x", "y"],
        ["-y", "z"],
        ["x", "-z"],
        ["z", "y"],
    ]
    clauses = [
        ["1", "-3"],
        ["-1", "2"],
        ["-2", "-3"],
        ['-41', '-13'],
    ]
result = is_satisfiable(clauses)
if result is None:
    print("UNSATISFIABLE")
else:
    print("SATISFIABLE")
    print(" ".join(result[i] for i in range(len(result))))
