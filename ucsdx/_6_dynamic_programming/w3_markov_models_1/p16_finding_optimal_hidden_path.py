# python3
import sys


def optimal_path(x, sigma, states, transition, emission):
    """Computes the optimal path through an HMM given an emitted string

    Args:
        x: A string containing the outcome
        sigma: A list of strings containing the HMM alphabet
        states: A list of strings containing all possible states
        transition: A 2D dictionary s.t. transition[x][y] is the
            probability of transitioning from state x to state y.
        emission: A 2D dictionary s.t. emission[x][y] is the
            probability of emitting letter y from state x.

    Returns:
        A string containing the optimal path
    """
    # TODO: your code here
    paths = [{state: (1.0 / len(states) * emission[state][x[0]], None) for state in states}]
    for output in x[1:]:
        new_path = {}
        for target_state in states:
            possible_origins = [(paths[-1][source_state][0] * transition[source_state][target_state], source_state) for source_state in states]
            best_transition_score, parent = max(possible_origins, key=lambda p: p[0])
            new_path[target_state] = (best_transition_score * emission[target_state][output], parent)
        paths.append(new_path)
    best_path = [max([state for state in paths[0]], key=lambda s: paths[-1][s][0])]
    for i in range(len(paths)-1, 0, -1):
        best_path.append(paths[i][best_path[-1]][1])
    best_path.reverse()
    return ''.join(best_path)  # + '##' + str(paths[-1][best_path[-1]][0])


if __name__ == "__main__":
    x = sys.stdin.readline().strip()
    sys.stdin.readline()  # delimiter

    sigma = sys.stdin.readline().strip().split()
    sys.stdin.readline()  # delimiter

    states = sys.stdin.readline().strip().split()
    sys.stdin.readline()  # delimiter

    chars = sys.stdin.readline().strip().split()
    transition = [sys.stdin.readline().strip().split() for _ in range(len(states))]
    transition = {line[0]: dict(zip(chars, map(float, line[1:]))) for line in transition}
    sys.stdin.readline()  # delimiter

    chars = sys.stdin.readline().strip().split()
    emission = [sys.stdin.readline().strip().split() for _ in range(len(states))]
    emission = {line[0]: dict(zip(chars, map(float, line[1:]))) for line in emission}

    print(optimal_path(x, sigma, states, transition, emission))
