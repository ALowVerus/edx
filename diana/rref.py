from fractions import Fraction


def solve(system: str) -> str:
    system = [[Fraction(f) for f in line.split(" ")] for line in system.split('\n')]
    print('\nINITIAL:')
    for line in system:
        print(['{:>5}'.format(str(f)) for f in line])
    # Get to echelon form
    r, c = 0, 0
    while r < len(system) and c < len(system[0]) - 1:
        if system[r][c] == 0:
            r2 = r
            while r2 < len(system) and system[r2][c] == 0:
                r2 += 1
            if r2 < len(system):
                system[r], system[r2] = system[r2], system[r]
            else:
                c += 1
        else:
            # Reduce leading column factors to 1
            for r2 in range(r, len(system)):
                if system[r2][c] != 1 and system[r2][c] != 0:
                    for c2 in range(c+1, len(system[0])):
                        system[r2][c2] /= system[r2][c]
                    system[r2][c] /= system[r2][c]
            # Subtract reduce from the ranking row down
            for r2 in range(r+1, len(system)):
                if system[r2][c] == 1:
                    for c2 in range(c, len(system[0])):
                        system[r2][c2] -= system[r][c2]
            r += 1
            c += 1
#     print('\nECHELON:')
#     for line in system:
#         print(['{:>5}'.format(str(f)) for f in line])
    # Get to row reduced echelon form
    for r in range(len(system)-1, -1, -1):
        c = 0
        while c < len(system[0]) and system[r][c] == 0:
            c += 1
        if c < len(system[0]):
            for r2 in range(r):
                if system[r2][c] != 0:
                    # Multiply the source row by the factor of the target
                    for c2 in range(c, len(system[0])):
                        system[r][c2] *= system[r2][c]
                    # Subtract the source row from the target row
                    for c2 in range(c, len(system[0])):
                        system[r2][c2] -= system[r][c2]
                    # Divide the source row by the factor of the target
                    for c2 in range(c+1, len(system[0])):
                        system[r][c2] /= system[r][c]
                    system[r][c] /= system[r][c]
    print('\nRREF:')
    for line in system:
        print(['{:>5}'.format(str(f)) for f in line])
    # Determine whether there is no solution
    for line in system:
        if sum([line[i] != 0 for i in range(len(line)-1)]) == 0 and line[-1] != 0:
            return "SOL=NONE"
    # Track the matrix dimensions, in case the matrix is a null
    n, m = len(system), len(system[0])
    # Pop out null lines
    while len(system) > 0 and sum([item != 0 for item in system[-1]]) == 0:
        system.pop()
    # If we've hit a null matrix, act appropriately
    if len(system) == 0:
        return "SOL=NONE"
    # Print the reduced matrix
    print('\nRREF:')
    for line in system:
        print(['{:>5}'.format(str(f)) for f in line])
    parts = {}
    for line in system:
        root_i = 0
        while line[root_i] == 0:
            root_i += 1
        for j in range(root_i+1, len(line)):
            if j not in parts:
                parts[j] = [Fraction(0) for var in range(len(system[0]) - 1)]
            if line[j] != 0:
                parts[j][root_i] -= line[j]
    for n in parts:
        if n != len(system[0]) - 1:
            parts[n][n] = 1
    parts = {'({})'.format()}
    res = 'SOL= (0; 0; 0) + q1 * (0; 0; 0) + q2 * (0; 0; 0) + q3 * (0; 0; 0)'
    print('\n', res)
    return res