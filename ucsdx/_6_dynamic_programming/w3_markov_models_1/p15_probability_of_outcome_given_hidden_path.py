# python3
import sys


def outcome_probability(x, sigma, pi, states, emission):
    """Computes probability of an an outcome x given a path pi and an emission matrix.

    Make sure that your output is to at least three significant figures.

    Args:
        x: A string containing the outcome
        sigma: A list of strings containing the HMM alphabet
        pi: A string containg the path.
        states: A list of strings containing all possible states
        emission: A 2D dictionary s.t. emission[x][y] is the
            probability of emitting letter y from state x.

    Returns:
        A float with the probability to at least three significant figures.
    """
    # TODO: your code here
    p = 1.0
    for step_state, step_emission in zip(pi, x):
        p *= emission[step_state][step_emission]
    return p


if __name__ == "__main__":
    x = sys.stdin.readline().strip()
    sys.stdin.readline()  # delimiter

    sigma = sys.stdin.readline().strip().split()
    sys.stdin.readline()  # delimiter

    pi = sys.stdin.readline().strip()
    sys.stdin.readline()  # delimiter

    states = sys.stdin.readline().strip().split()
    sys.stdin.readline()  # delimiter

    chars = sys.stdin.readline().strip().split()
    emission = [sys.stdin.readline().strip().split() for _ in range(len(states))]
    emission = {line[0]: dict(zip(chars, map(float, line[1:]))) for line in emission}

    print(outcome_probability(x, sigma, pi, states, emission))
