# python3
import sys
from itertools import chain


def estimate_transition_matrix(pi):
    adj = {}
    for i in range(len(pi)-1):
        start, end = pi[i], pi[i+1]
        load(adj, start, end, 1)
    fractionalize(adj)
    return adj


def estimate_emission_matrix(x, pi):
    emission = {}
    for output, state in zip(x, pi):
        load(emission, state, output, 1)
    fractionalize(emission)
    return emission


def load(a, r, c, amount=1):
    if r not in a:
        a[r] = {}
    if c not in a[r]:
        a[r][c] = 0
    a[r][c] += amount


def fractionalize(a, pseudocount=0):
    for r in a:
        if len(a[r]) > 0:
            total = sum([item for key, item in a[r].items()])
            a[r] = {k: ((v / total) + pseudocount) / (1 + len(a[r]) * pseudocount) if total > 0 else 1.0 / len(a[r])
                    for k, v in a[r].items()}


def profile_hmm(theta, sigma, alignment, pseudocount):
    """Creates a profile HMM from a multiple alignment.

    Args:
        theta: A float threshold for the seed alignment
        sigma: A list of strings containing the HMM alphabet
        alignment: A list of strings containing the multiple alignment
            for which the profile HMM will be constructed
        pseudocount: A float value containing the pseudocount to be added

    Returns:
        A string with the emission and transition matrices formatted
            according to the problem output specification.
    """
    # TODO: your code here
    # Count the columns
    col_count = len(alignment[0])
    # Figure out which columns are valid
    is_valid = [sum([s[i] == '-' for s in alignment]) / len(alignment) < theta for i in range(col_count)]

    # Get a sparse adjacency matrix
    if sum(is_valid) == 0:
        raise Exception('There are no valid columns.')
    # Generate a state adjacency matrix
    adj = {}
    for path in alignment:
        i = 0
        layer = 0
        latest_hit = 'S'
        while i < len(is_valid):
            if is_valid[i]:
                layer += 1
                target = ('D' if path[i] == '-' else 'M') + str(layer)
                load(adj, latest_hit, target)
                latest_hit = target
            elif path[i] != '-':
                target = 'I' + str(layer)
                load(adj, latest_hit, target)
                latest_hit = target
            i += 1
        load(adj, latest_hit, 'E')
    if pseudocount > 0:
        layer = sum(is_valid)
        for r in ['S', 'I0']:
            for c in ['I0', 'M1', 'D1']:
                load(adj, r, c, 0)
        for layer_i in range(1, sum(is_valid)):
            for r in "M{} D{} I{}".format(layer_i, layer_i, layer_i).split(' '):
                for c in "I{} M{} D{}".format(layer_i, layer_i + 1, layer_i + 1).split(' '):
                    load(adj, r, c, 0)
        for r in "M{} D{} I{}".format(layer, layer, layer).split(' '):
            load(adj, r, 'I{}'.format(layer), 0)
            load(adj, r, 'E', 0)
    # Generate a letter frequency matrix
    letter_frequency = {}
    layer = 0
    for i in range(col_count):
        layer += int(is_valid[i])
        for path in alignment:
            if path[i] != '-':
                load(letter_frequency,
                     ('M' if is_valid[i] else 'I') + str(layer),
                     path[i])
    if pseudocount > 0:
        for i in range(sum(is_valid) + 1):
            for c in sigma:
                load(letter_frequency, 'I' + str(i), c, 0)
                if i > 0:
                    load(letter_frequency, 'M' + str(i), c, 0)
    # Convert the count matrices to fractional matrices
    fractionalize(adj, pseudocount)
    fractionalize(letter_frequency, pseudocount)
    # Print the spare transmission matrix
    node_names = ['S', 'I0'] + list(chain(*[[c + str(i) for c in "MDI"] for i in range(1, layer + 1)])) + ['E']
    return adj, letter_frequency, node_names, sigma


# Use the following output commands for p18 and p19
def format_matrix_as_string(m, row_headings, col_headings):
    lines = [' '.join(col_headings)]
    for source in row_headings:
        parts = [source]
        for target in col_headings:
            if source in m and target in m[source]:
                parts.append(str(m[source][target]))
            else:
                parts.append('0')
        lines.append(' '.join(parts))
    return '\n'.join(lines)


def format_emission_answer(adj, letter_frequency, node_names, sigma):
    transmission = format_matrix_as_string(adj, node_names, node_names)
    output = format_matrix_as_string(letter_frequency, node_names, sigma)
    return '\n--------\n'.join([transmission, output])


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
    layer_count = len(states) // 3
    # Find the correct path
    e = lambda r, c: emission[r][c] if r in emission and c in emission[r] else 0
    t = lambda r, c: transition[r][c] if r in transition and c in transition[r] else 0
    paths = {'S': {0: (1.0, None)}, 'I0': {0: (0.0, None), 1: (e('I0', x[0]) * t('S', 'I0'), 'S')}}
    for source in states:
        if source not in paths:
            paths[source] = {}
    p = lambda n, i: paths[n][i][0] if n in paths and i in paths[n] else 0
    for i in range(1, len(x)):
        paths['I0'][i+1] = (p('I0', i - 1) * e('I0', x[i]) * t('I0', 'I0'), 'I0')
    for layer_i in range(1, layer_count):
        dc, ic, mc, dp, ip, mp = "D{} I{} M{} D{} I{} M{}". \
            format(layer_i, layer_i, layer_i, layer_i - 1, layer_i - 1, layer_i - 1). \
            split(' ')
        # Update the M and D nodes
        if layer_i == 1:
            for i in range(0, len(x)+1):
                if i == 0:
                    paths['D1'][0] = (1.0 * t('S', 'D1'), 'S')
                    paths['M1'][0] = (0.0, 'S')
                else:
                    paths['D1'][i] = (p('I0', i) * t('I0', 'D1'), 'I0')
                    if i == 1:
                        paths['M1'][i] = (p('S', 0) * t('S', 'M1'), 'S')
                    else:
                        paths['M1'][i] = (p('I0', i - 1) * t('I0', 'M1'), 'I0')
        else:
            for i in range(0, len(x)+1):
                dc_options = [(p(dp, i) * t(dp, dc), dp), (p(ip, i) * t(ip, dc), ip), (p(mp, i) * t(mp, dc), mp)]
                paths[dc][i] = max(dc_options, key=lambda p: p[0])
                mc_options = [(p(dp, i-1) * t(dp, mc), dp), (p(ip, i-1) * t(ip, mc), ip), (p(mp, i-1) * t(mp, mc), mp)]
                mc_chosen = max(mc_options, key=lambda p: p[0])
                paths[mc][i] = (mc_chosen[0] * e(mc, x[i-1]), mc_chosen[1])
        # Update the I node
        for i in range(1, len(x) + 1):
            ic_options = [(p(dc, i-1) * t(dc, ic), dc), (p(mc, i-1) * t(mc, ic), mc)]
            ic_chosen = max(ic_options, key=lambda p: p[0])
            paths[ic][i] = (ic_chosen[0] * e(ic, x[i-1]), ic_chosen[1])
    dp, ip, mp = "D{} I{} M{}".format(layer_count-1, layer_count-1, layer_count-1).split(' ')
    for i in range(0, len(x) + 1):
        paths['E'][i] = max([(p(dp, i), dp), (p(ip, i), ip), (p(mp, i), mp)], key=lambda p: p[0])
    # Get the best path value at the end
    best_path = [('E', len(x))]
    while best_path[-1] != ('S', 0):
        node, i = best_path[-1]
        predecessor = paths[node][i][1]
        best_path.append((predecessor, i - (1 if node[0] in "IM" else 0)))
    best_path = [item[0] for item in best_path]
    return ' '.join(best_path[::-1][1:-1])


if __name__ == "__main__":
    problem_number = 21
    if problem_number in {18, 19, 20}:
        if problem_number == 20:
            x = sys.stdin.readline().strip()
            sys.stdin.readline()  # delimiter
        else:
            x = None
        if problem_number in {19, 20}:
            theta, pseudocount = map(float, sys.stdin.readline().strip().split())
        elif problem_number == 18:
            theta, pseudocount = float(sys.stdin.readline().strip()), 0
        else:
            raise Exception()
        sys.stdin.readline()  # delimiter
        sigma = sys.stdin.readline().strip().split()
        sys.stdin.readline()  # delimiter
        alignment = [line.strip() for line in sys.stdin]


        # # Test 1
        # x = 'AB'
        # theta, pseudocount = 0.4, 0.01
        # sigma = ['A', 'B']
        # alignment = ['AA', 'AA']

        # # Test 2
        # x = 'AB'
        # theta, pseudocount = 0.4, 0.01
        # sigma = ['A', 'B', 'C', 'D', 'E']
        # alignment = ['AA', 'AA']

        # # Test 3
        # x = 'AB'
        # theta, pseudocount = 0.4, 0.01
        # sigma = ['A', 'B']
        # alignment = ['A-', 'A-']

        # # Test 4
        # x = 'AAAAAB'
        # theta, pseudocount = 0.4, 0.01
        # sigma = [c for c in 'AB']
        # alignment = [
        #     '-B',
        #     '-B',
        # ]

        # # Test 5
        # x = 'AB'
        # theta, pseudocount = 0.4, 0.01
        # sigma = [c for c in 'AB']
        # alignment = [
        #     'AAAAB',
        #     'AAAAB',
        # ]

        # x = 'AEFDFDC'
        # theta, pseudocount = 0.4, 0.01
        # sigma = [c for c in 'ABCDEF']
        # alignment = [
        #     'ACDEFACADF',
        #     'AFDA---CCF',
        #     'A--EFD-FDC',
        #     'ACAEF--A-C',
        #     'ADDEFAAADF',
        # ]

        state_adjacency_matrix, emission_probability_matrix, node_names, sigma = \
            profile_hmm(theta, sigma, alignment, pseudocount)

        if problem_number in {18, 19}:
            print(format_emission_answer(state_adjacency_matrix,
                                         emission_probability_matrix,
                                         node_names, sigma))
        if problem_number == 20:
            print(optimal_path(x, sigma, node_names,
                               state_adjacency_matrix,
                               emission_probability_matrix))

    elif problem_number == 21:
        """Estimates parameters for a HMM

        Args:
            x: A string emitted by the HMM
            sigma: A list of strings containing the HMM alphabet
            pi: A string hidden path emitted by the HMM
            states: A list of strings containing the possible states for the HMM

        Returns:
            The emission and transition matrices formatted as specified in the
            problem
        """
        x = sys.stdin.readline().strip()
        sys.stdin.readline()  # delimiter
        sigma = sys.stdin.readline().strip().split()
        sys.stdin.readline()  # delimiter
        pi = sys.stdin.readline().strip()
        sys.stdin.readline()  # delimiter
        states = sys.stdin.readline().strip().split()

        # x = 'xyy'
        # sigma = ['x', 'y']
        # pi = 'AAA'
        # states = ['A']

        transition = estimate_transition_matrix(pi)
        for source_state in states:
            if source_state not in transition:
                transition[source_state] = {target_state: 1.0 / len(states) for target_state in states}
        emission = estimate_emission_matrix(x, pi)
        for source_state in states:
            if source_state not in emission:
                emission[source_state] = {symbol: 1.0 / len(sigma) for symbol in sigma}

        print(format_emission_answer(transition, emission, states, sigma))

