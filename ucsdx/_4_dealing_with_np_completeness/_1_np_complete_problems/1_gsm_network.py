#python3
# Input some lines
n, m = map(int, input().split())
edges = [tuple(map(int, input().split())) for i in range(m)]
# Convert into a dictionary of vertices
adj = {}
for (i0, i1) in edges:
    if i0 not in adj:
        adj[i0] = set()
    adj[i0].add(i1)
    if i1 not in edges:
        adj[i1] = set()
    adj[i1].add(i0)
# Initialize a list of checks
checks = set()
# No vertex may have more than 1 color
for v in range(1, n+1):
    checks.add("{} {} {}".format(v, v + n, v + n * 2))
    checks.add("-{} -{}".format(v    , v + n    ))
    checks.add("-{} -{}".format(v    , v + n * 2))
    checks.add("-{} -{}".format(v + n, v + n * 2))
# No two adjacent vertices may have
for v in adj:
    for t in adj[v]:
        a, b = sorted([v, t])
        checks.add("-{} -{}".format(a, b))
        checks.add("-{} -{}".format(a + n, b + n))
        checks.add("-{} -{}".format(a + n * 2, b + n * 2))
# Add a null case.
if len(checks) == 0:
    checks.add("1")
# Return the checks!
print("{} {}".format(len(checks), n * 3))
for check in checks:
    print(check, "0")
