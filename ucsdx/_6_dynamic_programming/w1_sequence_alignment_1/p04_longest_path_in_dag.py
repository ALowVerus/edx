# python3
import re
import sys
import threading

sys.setrecursionlimit(10 ** 7)  # max depth of recursion
threading.stack_size(2 ** 30)  # new thread will get stack of such size


def longest_path(source, sink, edges):
    """
    source is the integer source node label
    sink is the integer sink node lable
    edges is a string list of the edges from the input file

    return a string containing the output in the correct format
    """
    if source == sink:
        return 0, []
    # Generate adjacency structure
    adj = {}
    for edge in edges:
        s, t, c = re.match(r'(\-?[0-9]+)->(\-?[0-9]+):(\-?[0-9]+)', edge).groups()
        s, t, c = int(s), int(t), int(c)
        if s not in adj:
            adj[s] = {}
        adj[s][t] = c
    # Generate a set of in-edges for each node
    in_edges = {}
    for s in adj:
        if s not in in_edges:
            in_edges[s] = set()
        for t in adj[s]:
            if t not in in_edges:
                in_edges[t] = set()
            in_edges[t].add(s)
    # Recursively generate the best scores
    best_scores = {source: (None, 0)}
    def recurse(node):
        parent_node, score = best_scores[node]
        if node in adj:
            for child, cost in adj[node].items():
                in_edges[child].remove(node)
                if child not in best_scores:
                    best_scores[child] = (node, score + cost)
                elif score + cost > best_scores[child][1]:
                    best_scores[child] = (node, score + cost)
                if len(in_edges[child]) == 0:
                    recurse(child)
    recurse(source)
    # print(best_scores)
    # Get a path and cost
    path = []
    curr = sink
    while curr is not None:
        path.append(curr)
        curr = best_scores[curr][0]
    # Return a properly-formatted result
    return best_scores[sink][1], path[::-1]


test_cases = [
    ('Sample Data',
        0, 4, "0->1:7\n0->2:4\n2->3:2\n1->4:1\n3->4:3", 9),
    ('Test case 1',
        0, 3, "0->1:1\n1->2:1\n2->3:3\n0->3:10", 10),
    ('Test case 2',
        0, 3, "0->1:2\n0->2:1\n1->3:3\n2->3:3", 5),
    ('Test case 3',
        0, 3, "0->1:1\n0->2:5\n1->3:10\n2->3:1", 11),
    ('Test case 4',
        1, 4, "1->2:1\n1->3:5\n2->4:10\n3->4:1", 11),
    ('Test case 5',
        1, 10, "1->2:1\n2->3:3\n3->10:1", 5),
    ('Test case 6',
        0, 4, "0->4:7", 7),
    ('Multiple paths #1',
        0, 4, "0->4:4\n0->1:1\n0->2:2\n0->3:3\n1->4:3\n1->3:2\n1->2:1\n2->3:1\n2->4:2\n3->4:1", 4),
    ('Negative Distances',
        0, 4, "0->1:-1\n0->2:-3\n0->3:-5\n0->4:-4\n1->2:2\n2->3:-5\n2->4:-10\n3->4:2", -2),
    ('Negative node numbers',
        -3, 0, "-3->-2:-1\n-2->0:1\n-3->0:3", 3),
    ('Starting node > minimum node number',
        1, 3, "0->1:1\n1->2:1\n2->3:1\n0->3:3", 2),
    ('Single node',
        0, 0, "", 0),
    ('Ending node < greatest node number',
        0, 3, "0->1:3\n0->2:2\n0->4:3\n1->2:3\n1->3:5\n2->3:2\n2->4:3\n2->5:1\n3->5:1", 8),
    ('Starting and ending nodes are the same',
        3, 3, "0->1:3\n0->2:2\n0->4:3\n1->2:3\n1->3:5\n2->3:2\n2->4:3\n2->5:1\n3->5:1", 0),
    ('Multiple paths #2',
        0, 4, "0->4:4\n0->1:1\n0->2:2\n0->3:3\n1->4:3\n1->3:2\n1->2:1\n2->3:2\n2->4:3\n3->4:1", 5),
    ('Negative nodes, negative weights',
        -4, -1, "-5->-4:-4\n-4->-3:-10\n-4->-2:-2\n-3->-1:-1\n-3->-2:-15\n-2->-1:-5", -7),
]

# exceptions = []
# for name, source, sink, edge_text, true_cost in test_cases:
#     edges = edge_text.split('\n')
#     try:
#         predicted_cost, predicted_path = longest_path(source, sink, edges)
#         print(predicted_cost == true_cost, name)
#     except Exception as e:
#         print(name, 'has failed.')
#         exceptions.append(e)
# for e in exceptions:
#     raise e


if __name__ == "__main__":
    source = int(sys.stdin.readline().strip())
    sink = int(sys.stdin.readline().strip())
    edges = [line.strip() for line in sys.stdin]
    best_cost, best_path = longest_path(source, sink, edges)
    print('{}\n{}'.format(best_cost, '->'.join(map(str, best_path))))
