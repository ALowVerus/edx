# python3

from copy import deepcopy

pieces = """
    (yellow,black,black,blue)
    (blue,blue,black,yellow)
    (orange,yellow,black,black)
    (red,black,yellow,green)
    (orange,green,blue,blue)
    (green,blue,orange,black)
    (black,black,red,red)
    (black,red,orange,purple)
    (black,purple,green,black)
""".split('\n')[1:-1]
pieces = [piece.strip()[1:-1].split(',') for piece in pieces]
pieces = [input()[1:-1].split(',') for i in range(25)]
n = int(len(pieces) ** 0.5)


def assemble_puzzle(row_count, col_count, pieces):
    # print('Square size:', n)
    colors = set.union(*[set(piece) for piece in pieces])
    # print('Pieces:\n\t', '\n\t'.join(["{}: ".format(i) + ', '.join(piece) for i, piece in enumerate(pieces)]))
    # print('Colors:', colors)


    # Macro the pushing procedure
    def push(a, r, c, v):
        if r not in a:
            a[r] = {}
        if c not in a[r]:
            a[r][c] = set()
        a[r][c].add(v)


    # Figure out where each item is facing
    facings = {}
    for i, (u, l, d, r) in enumerate(pieces):
        push(facings, 'u', u, i)
        push(facings, 'l', l, i)
        push(facings, 'd', d, i)
        push(facings, 'r', r, i)

    # Parse out the parts of the board
    black_counts = [sum([side == 'black' for side in pieces[i]]) for i in range(len(pieces))]
    corners = [i for i in range(len(pieces)) if black_counts[i] == 2]
    corners = sorted([[int(pieces[i][j] == 'black') for j in range(4)] + [i] for i in corners])
    br, bl, ur, ul = [{corners[i][4]} for i in range(4)]
    sides = {i for i in range(len(pieces)) if black_counts[i] == 1}
    sides_u = {i for i in sides if pieces[i][0] == 'black'}
    sides_l = {i for i in sides if pieces[i][1] == 'black'}
    sides_d = {i for i in sides if pieces[i][2] == 'black'}
    sides_r = {i for i in sides if pieces[i][3] == 'black'}
    inners = {i for i in range(len(pieces)) if black_counts[i] == 0}

    # print('BR:', br)
    # print('BL:', bl)
    # print('UL:', ul)
    # print('UR:', ur)
    # print('Sides_U:', sides_u)
    # print('Sides_L:', sides_l)
    # print('Sides_D:', sides_d)
    # print('Sides_R:', sides_r)
    # print('Inner squares:', inners)

    list_assignments = []
    for i in range(n):
        for j in range(n):
            if i == 0 and j == 0:
                list_assignments.append(ul)
            elif i == 0 and j == n - 1:
                list_assignments.append(ur)
            elif i == n - 1 and j == 0:
                list_assignments.append(bl)
            elif i == n - 1 and j == n - 1:
                list_assignments.append(br)
            elif i == 0:
                list_assignments.append(sides_u)
            elif i == n - 1:
                list_assignments.append(sides_d)
            elif j == 0:
                list_assignments.append(sides_l)
            elif j == n - 1:
                list_assignments.append(sides_r)
            else:
                list_assignments.append(inners)


    # Dynamically fill the board sides, then work our way in
    board = [[None for c in range(n)] for r in range(n)]


    def recurse(r, c):
        r += c // n
        c %= n
        i = r * n + c
        if r == n:
            # print(i * ' ', "Success!")
            return True
        options_list_copy = deepcopy(list_assignments[r * n + c])
        # print(i * ' ', "Iterating over r, c=", r, c, options_list_copy)
        # for line in board:
        #     print(i * ' ', line)
        for option in options_list_copy:
            u_fits = ((r == 0 and pieces[option][0] == 'black') or (
                            r > 0 and pieces[option][0] == pieces[board[r - 1][c]][2]))
            l_fits = ((c == 0 and pieces[option][1] == 'black') or (
                            c > 0 and pieces[option][1] == pieces[board[r][c - 1]][3]))
            d_fits = ((r == n - 1 and pieces[option][2] == 'black') or (r < n and pieces[option][2] != 'black'))
            r_fits = ((c == n - 1 and pieces[option][3] == 'black') or (c < n and pieces[option][3] != 'black'))
            # print(i * ' ', option, u_fits, l_fits, d_fits, r_fits)
            if l_fits and u_fits and d_fits and r_fits:
                list_assignments[r * n + c].remove(option)
                board[r][c] = option
                res = recurse(r, c + 1)
                if res:
                    return True
                list_assignments[r * n + c].add(option)
                board[r][c] = None
        # print(i * ' ', "Failed at", r, c)
        return False


    recurse(0, 0)

    return None if board[-1][-1] is None else board


board = assemble_puzzle(n, n, pieces)
if not board:
    raise Exception
for line in board:
    print(';'.join(['({})'.format(','.join(pieces[tile_index])) for tile_index in line]))
