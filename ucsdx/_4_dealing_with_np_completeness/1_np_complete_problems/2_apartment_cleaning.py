#python3
# Try running graph from https://graphonline.ru/en/
from random import randint, shuffle


# The deterministic Bellman-Held-Karp algo, with its n^2 * 2^n complexity, never fails. It also takes an aeon to run.
def bellman_held_karp(possibilities):
    # Get a variable for the length of the items to save space
    n = len(possibilities)
    # Instantiate an array to hold referral information
    array = []
    # For every subset of n items, there being 2 ** n of them
    for j in range(2 ** n):
        row = []
        # For each item in the n items
        for i in range(n):
            # Add an entry for whether we can end at that point
            row.append(0)
        array.append(row)
    # For every item, set the subset of size 1 that contains it.
    # We can do this i, 2**i notation because the subsets are arranged like so:
    # a, b, ab, c, ac, bc, abc, d, ...
    # which means that all the information required to check the next item is already given, in all cases
    for i in range(n):
        array[2 ** i][i] = i + 1
    # Which iterating over all subsets
    for i in range(2 ** n):
        # And all the possible endpoints for those subsets
        for j in range(n):
            # If the j-th bit in i in set; i.e. if we have started to consider the item at hand.
            # We do this because of the way we have set up the bit-masking such that each bit matches a new item.
            # i.e. the first subset in 2 ** i is a, the second is b, the fourth c, the 8th d.
            # To account for this, we must start our indexing at 1, so 1 is a.
            # If 0 is a, these shenanigans fail.
            if i & (2 ** j):
                # We know that j is up for consideration, so we can now check its precursors.
                for k in range(n):
                    # If A) the subset at hand contains the precursor
                    # and B) the precursor is linked to j,
                    if i & (2 ** k) and k in [item - 1 for item in possibilities[j + 1]]:
                        # If the subset that leads to j can be visited,
                        if array[i ^ (2 ** j)][k]:
                            # We can visit this subset. Record so.
                            array[i][j] = k + 1
    # If any of the items in the final set, which represents the full set, are True, we found a good end.
    for j in range(n):
        if array[(2 ** n) - 1][j]:
            result = []
            count = 0
            my_next = j + 1
            x = (2 ** n) - 1
            while x > 0 and count < n:
                result.append(my_next)
                my_next = array[x][my_next - 1]
                x = x ^ (2 ** (result[-1] - 1))
                count += 1
            return result
    return False


# The random-guessing Posa-Ran algo is a Monte Carlo that fails with 25% certainty at each triangle.
def posa_ran(possibilities):
    #     print_possibilities(possibilities)
    for i in range(5000):
        # Set pivot counts to avoid infinite looping
        pivot_limit = len(possibilities)
        pivot_count = 0
        # Iterate over the nodes, looking for a path
        path = [randint(1, len(possibilities))]
        seen = {path[0]}
        #         print(seen, path, possibilities)
        while pivot_count < pivot_limit and len(path) < len(possibilities):
            # Attempt to find an edge that passes to a new node
            next_options = set(possibilities[path[-1]])
            done = False
            while not done and len(next_options) > 0:
                option = next_options.pop()
                if option not in seen:
                    path.append(option)
                    seen.add(option)
                    done = True
            # If no new node was found, pivot the list
            if not done:
                options = [item for item in set(possibilities[path[-1]])]
                shuffle(options)
                pivot_node = options[0]
                pivot_index = path.index(pivot_node)
                new_path = path[:pivot_index + 1] + path[pivot_index + 1:][::-1]
                #                 print("NO PATH FORWARD FROM {}. PIVOTING AT {}.\n Original: {};\n New: {}"
                #                         .format(path[-1], path[pivot_index], path, new_path))
                path = new_path
                pivot_count += 1
        if pivot_count < pivot_limit:
            return path
        print("Bad run", i + 1)
    return False


def exhaustive(n, possibilities):
    def guess(root, possibilities, indent=0):
        for possibility in possibilities[root[-1]]:
            if possibility not in root:
                result = work(root + [possibility], possibilities, indent)
                if result:
                    return result
        return False

    def work(root, possibilities, indent=0):
        my_root = root.copy()
        while len(my_root) <= len(possibilities):
            if len(my_root) == len(possibilities):
                return my_root
            if len(possibilities[my_root[-1]] - set(my_root)) == 0:
                return False
            if len(possibilities[my_root[-1]] - set(my_root)) > 1:
                return guess(my_root, possibilities, indent + 1)
            else:
                my_root.append(next(iter(possibilities[my_root[-1]] - set(my_root))))

    single_entries = [i for i in range(1, n + 1) if len(possibilities[i]) == 1]
    if len(single_entries) > 2:
        return False
    elif len(single_entries) > 0:
        return work(single_entries[-1:], possibilities)
    else:
        for possibility in possibilities:
            result = work([possibility], possibilities)
            if result:
                return result
        return False


def search_solve(adj):
    # Check whether a solution is possible
    if len(adj) <= 5:
        res = bellman_held_karp(adj)
    else:
        res = posa_ran(adj)
    # Initialize a set of checks
    if res:
        print('1 1')
        print('1 0')
    else:
        print('2 1')
        print('1 0')
        print('-1 0')


def intended_solve(adj, n):
    if n == 0 or n == 1:
        print('1 1')
        print('1 0')
    elif len(adj) < n:
        print('2 1')
        print('1 0')
        print('-1 0')
    else:
        # Initialize a set of checks
        checks = set()
        # Generate a dictionary that can be referenced to get variable numberings, one for each loc-node combination
        cnd = {}
        for v in range(n):
            for i in range(n):
                cnd[(v, i)] = v + n * i + 1
        # Each vertex belongs to the path.∙
        for v in adj:
            checks.add("{} 0".format(" ".join([str(cnd[(v, i)]) for i in range(n)])))
        # Each vertex appears just once in a path - no vertex can have two indices true simultaneously
        for v in range(n):
            for i in range(n):
                for j in range(i+1, n):
                    checks.add("-{} -{} 0".format(cnd[(v, i)], cnd[(v, j)]))
        # Each number position in the path has an associated vertex - one index must be true for each vertex
        for i in range(n):
            checks.add("{} 0".format(" ".join([str(cnd[(v, i)]) for v in range(n)])))
        # No two vertices occupy the same position of a path.
        for i in range(n):   # For each index
            for v0 in range(n):          # For each vertex combo
                for v1 in range(v0+1, n):
                    checks.add("-{} -{} 0".format(cnd[(v0, i)], cnd[(v1, i)]))
        # Two successive vertices on a path must be connected by an edge.
        for v0 in range(n):              # For each vertex combo
            for v1 in range(v0+1, n):
                if v1 not in adj[v0]:      # If the vertices don't neighbor, it cannot be that (v0 and v1)
                    for i in range(n-1):
                        checks.add("-{} -{} 0".format(cnd[v0, i], cnd[v1, i + 1]))
                        checks.add("-{} -{} 0".format(cnd[v1, i], cnd[v0, i + 1]))
        # Print results!
        print("{} {}".format(len(checks), n ** 2))
        for check in checks:
            print(check)


n, m = map(int, input().split())
edges = [tuple(list(map(int, input().split()))) for i in range(m)]
# Convert into a dictionary of vertices
adj = {}
for i0, i1 in edges:
    i0, i1 = i0-1, i1-1
    if i0 not in adj:
        adj[i0] = set()
    adj[i0].add(i1)
    if i1 not in adj:
        adj[i1] = set()
    adj[i1].add(i0)
intended_solve(adj, n)
