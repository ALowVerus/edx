# python3
from collections import deque
import sys


def generate_circulation(node_count, lines, verbose=False):
    def print(*args):
        if verbose:
            for arg in args:
                sys.stdout.write(str(arg) + ' ')
            sys.stdout.write('\n')

    print("You have entered testing mode.")

    remaining_flow = {**{i: {} for i in range(node_count)}, **{'S': {}, 'T': {}}}
    back_flow = {**{i: {} for i in range(node_count)}, **{'S': {}, 'T': {}}}
    node_weights = [0 for i in range(node_count)]

    for s, t, min_c, max_c in lines:
        s, t = s - 1, t - 1
        if s != t:
            node_weights[s] -= min_c
            node_weights[t] += min_c
            if max_c > min_c:
                if t not in remaining_flow[s]:
                    remaining_flow[s][t] = 0
                remaining_flow[s][t] += max_c - min_c

    for node in range(node_count):
        if node_weights[node] > 0:
            remaining_flow['S'][node] = node_weights[node]
        elif node_weights[node] < 0:
            remaining_flow[node]['T'] = -node_weights[node]

    done = False
    # Repeat until no further addition is possible
    while not done:
        print('ROUND!', len(remaining_flow), len(back_flow))
        for s in remaining_flow:
            print('\t', s, remaining_flow[s], back_flow[s])
        # Do a BFS of the existing adjacency matrix to find a valid path to the target
        backtrackers = {'S': None}
        h = deque(['S'])
        while h and 'T' not in backtrackers:
            curr_node = h.popleft()
            for neighbor in remaining_flow[curr_node]:
                if neighbor not in backtrackers:
                    h.append(neighbor)
                    backtrackers[neighbor] = curr_node
            for neighbor in back_flow[curr_node]:
                if neighbor not in backtrackers:
                    h.append(neighbor)
                    backtrackers[neighbor] = curr_node
        if 'T' in backtrackers:
            print('Backtrackers:', backtrackers)
            curr = 'T'
            path = []
            while curr is not None:
                path.append(curr)
                curr = backtrackers[curr]
            path = path[::-1]
            print('Path:', path)
            min_cost = 10 ** 8
            for i in range(len(path) - 1):
                step_remaining_flow = remaining_flow[path[i]][path[i + 1]] if path[i + 1] in remaining_flow[path[i]] else 0
                step_back_flow = back_flow[path[i]][path[i + 1]] if path[i + 1] in back_flow[path[i]] else 0
                min_cost = min([min_cost, max([step_remaining_flow, step_back_flow])])
            if min_cost > 0:
                for i in range(len(path) - 1):
                    s, t = path[i:i + 2]
                    # Add blank edges in case they are needed
                    if t not in remaining_flow[s]:
                        remaining_flow[s][t] = 0
                    if s not in remaining_flow[t]:
                        remaining_flow[t][s] = 0
                    if t not in back_flow[s]:
                        back_flow[s][t] = 0
                    if s not in back_flow[t]:
                        back_flow[t][s] = 0
                    # Appropriately shift edge weights
                    c = min_cost
                    if remaining_flow[s][t] > 0:
                        cost_to_shift = min(c, remaining_flow[s][t])
                        c -= cost_to_shift
                        remaining_flow[s][t] -= cost_to_shift
                        back_flow[t][s] += cost_to_shift
                    if c > 0:
                        cost_to_shift = min(c, back_flow[s][t])
                        c -= cost_to_shift
                        back_flow[s][t] -= cost_to_shift
                        remaining_flow[t][s] += cost_to_shift
                    if c > 0:
                        raise Exception("You have untended cost to shift.")
                    # Remove nulls
                    if remaining_flow[s][t] == 0:
                        remaining_flow[s].pop(t)
                    if remaining_flow[t][s] == 0:
                        remaining_flow[t].pop(s)
                    if back_flow[s][t] == 0:
                        back_flow[s].pop(t)
                    if back_flow[t][s] == 0:
                        back_flow[t].pop(s)
            else:
                raise Exception("You found a min cost of 0. Something is wrong.")
        else:
            done = True
    # If not solution exists doesn't, print NO
    if len(remaining_flow['S']) > 0:
        return False, None
    # Else, print the YES, then the cost assigned to each edge
    else:
        print('Final adjacency graph:')
        for s in remaining_flow:
            print('\t', s, remaining_flow[s], back_flow[s])
        allocated_weights = []
        for s, t, min_c, max_c in lines:
            # print(s, t, min_c, max_c)
            s, t = s - 1, t - 1
            if s == t:
                allocated_weights.append(min_c)
            else:
                c = min_c
                # Add blank edges in case they are needed
                if t not in back_flow[s]:
                    back_flow[s][t] = 0
                if s not in back_flow[t]:
                    back_flow[t][s] = 0
                # Recognize warped costs and reduce them
                flow_to_be_removed = min([max_c - min_c, back_flow[t][s]])
                c += flow_to_be_removed
                back_flow[t][s] -= flow_to_be_removed
                allocated_weights.append(c)
                # Remove nulls
                if back_flow[s][t] == 0:
                    back_flow[s].pop(t)
                if back_flow[t][s] == 0:
                    back_flow[t].pop(s)
        # print(allocated_weights)
        return True, tuple(allocated_weights)


def test(truth, answer, lines, node_count):
    answer, proposed_costs = answer
    if (truth is answer is False) or (truth is None and answer is False):
        print('\033[1;32;14m PASSED! \033[0;38;14m')
    elif (truth is answer is True) or (truth is None and answer is True):
        if len(proposed_costs) != len(lines):
            raise Exception("\nYou do not have a cost for each given edge.\n{}, {}, {}"
                            .format(len(lines), len(proposed_costs), proposed_costs))
        for i, (proposed_cost, (s, t, min_c, max_c)) in enumerate(zip(proposed_costs, lines)):
            if not min_c <= proposed_cost <= max_c:
                raise Exception("Your proposed cost for edge {}, which is {}, lies not within {} and {}"
                                .format(i + 1, proposed_cost, min_c, max_c))
        node_costs = [0 for i in range(node_count)]
        for proposed_cost, (s, t, min_c, max_c) in zip(proposed_costs, lines):
            node_costs[s - 1] -= proposed_cost
            node_costs[t - 1] += proposed_cost
        failed_nodes = [i + 1 for i in range(node_count) if node_costs[i] != 0]
        if len(failed_nodes) > 0:
            msg = "\nYour proposed costs would leave nodes ({}) with unbalanced in-degrees and out-degrees."\
                  .format(', '.join(map(str, failed_nodes)))
            raise Exception('\n'.join([msg, str(proposed_costs)]))
        print('\033[1;32;14m PASSED! \033[0;38;14m')
    elif truth is not answer:
        raise Exception("Your proposed answer is {}, but the given answer is {}.".format(answer, truth))
    print()


if __name__ == '__main__':
    using_test_cases = False

    if not using_test_cases:
        node_count, edge_count = map(int, input().split(' '))
        lines = []
        for i in range(edge_count):
            line = input().split(' ')
            line = list(map(int, line))
            lines.append(line)
        works, path = generate_circulation(node_count, lines)
        if works:
            print('YES')
            for cost in path:
                print(cost)
        else:
            print('NO')
    else:
        print("Straight line:")
        node_count = 3
        lines = [
            (1, 2, 0, 3),
            (2, 3, 0, 3),
        ]
        truth = True
        answer = generate_circulation(node_count, lines)
        test(truth, answer, lines, node_count)

        print("Simple triangle:")
        node_count = 3
        lines = [
            (1, 2, 1, 3),
            (2, 3, 2, 4),
            (3, 1, 1, 2),
        ]
        truth = True
        answer = generate_circulation(node_count, lines)
        test(truth, answer, lines, node_count)

        print("Invalid triangle:")
        node_count = 3
        lines = [
            (1, 2, 1, 3),
            (2, 3, 2, 4),
            (1, 3, 1, 2),
        ]
        truth = False
        answer = generate_circulation(node_count, lines)
        test(truth, answer, lines, node_count)

        print("More complicated 4-node graph:")
        node_count = 4
        lines = [
            (1, 3, 1, 3),
            (1, 4, 1, 3),
            (2, 3, 1, 3),
            (2, 4, 1, 3),
            (3, 1, 1, 3),
            (4, 2, 1, 3),
        ]
        truth = True
        answer = generate_circulation(node_count, lines)
        test(truth, answer, lines, node_count)

        print("No edges:")
        node_count = 5
        lines = []
        truth = True
        answer = generate_circulation(node_count, lines)
        test(truth, answer, lines, node_count)

        print("Doubled edges:")
        node_count = 4
        lines = [
            (1, 3, 1, 3),
            (1, 4, 1, 3),
            (2, 3, 1, 3),
            (2, 4, 1, 3),
            (3, 1, 1, 3),
            (4, 2, 1, 3),
            (1, 3, 1, 3),
            (1, 4, 1, 3),
            (2, 3, 1, 3),
            (2, 4, 1, 3),
            (3, 1, 1, 3),
            (4, 2, 1, 3),
        ]
        answer = generate_circulation(node_count, lines)
        test(truth, answer, lines, node_count)

        print("Masturbatory edges:")
        node_count = 3
        lines = [
            (1, 1, 1, 3),
            (2, 2, 1, 3),
            (3, 3, 1, 3),
        ]
        truth = True
        answer = generate_circulation(node_count, lines)
        test(truth, answer, lines, node_count)

        print("Strange test case:")
        node_count = 5
        lines = [
            (1, 3, 0, 2),
            (2, 1, 0, 2),
            (3, 2, 2, 2),
            (4, 3, 0, 1),
            (4, 5, 0, 1),
            (5, 4, 1, 1),
        ]
        truth = None
        answer = generate_circulation(node_count, lines)
        test(truth, answer, lines, node_count)

        print("Random Tests:")
        from random import randint
        node_count = 3
        while node_count < 100:
            line_count = int(1.2 * node_count)
            min_cost = 1
            max_cost = 30
            for i in range(1000):
                lines = []
                for j in range(line_count):
                    min_bound, max_bound = sorted([randint(min_cost, max_cost), randint(min_cost, max_cost)])
                    lines.append((randint(1, node_count), randint(1, node_count), min_bound, max_bound))
                try:
                    answer = generate_circulation(node_count, lines)
                    test(None, answer, lines, node_count)
                except Exception as e0:
                    print('\033[1;31;14m FAILURE! {} Nodes. Please review the following messages: \033[0;37;14m'
                          .format(node_count))
                    print('LINES!')
                    for line in lines:
                        print(line)
                    try:
                        answer = generate_circulation(node_count, lines, verbose=True)
                        test(None, answer, lines, node_count)
                    except Exception as e1:
                        print('\033[1;31;14m Hit the exception again. \033[0;37;14m')
                        raise e1
            node_count += 3
