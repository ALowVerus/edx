# python3
import sys


def path_probability(pi, states, transition):
    """Computes probability of a path pi through a given HMM.

    Make sure that your output is to at least three significant figures.

    Args:
        pi: A string containg the path.
        states: A list of strings containing all possible states
        transition: A 2D dictionary s.t. transition[x][y] is the
            probability of transitioning from state x to state y.

    Returns:
        A float with the probability to at least three significant figures.
    """
    # TODO: your code here
    print('pi:', pi)
    print('states:', states)
    print('transition', transition)
    curr_state = pi[0]
    p = 1.0 / len(states)
    for next_state in pi[1:]:
        p *= transition[curr_state][next_state]
        curr_state = next_state
    return p


if __name__ == "__main__":
    pi = sys.stdin.readline().strip()
    sys.stdin.readline()  # delimiter

    states = sys.stdin.readline().strip().split()
    sys.stdin.readline()  # delimiter

    chars = sys.stdin.readline().strip().split()  # first row of trans mat
    transition = {line[0]: dict(zip(chars, map(float, line.strip().split()[1:])))
                  for line in sys.stdin}

    print(path_probability(pi, states, transition))
