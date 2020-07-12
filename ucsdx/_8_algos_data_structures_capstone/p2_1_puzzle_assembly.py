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
# pieces = [input()[1:-1].split(',') for i in range(25)]
n = int(len(pieces) ** 0.5)
colors = set.union(*[set(piece) for piece in pieces])
print('Pieces:', '\n\t'.join(["{}: ".format(i) + ', '.join(piece) for i, piece in enumerate(pieces)]))
print('Colors:', colors)


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
br, bl, ur, ul = [corners[i][4] for i in range(4)]
sides = [i for i in range(len(pieces)) if black_counts[i] == 1]
sides_u = [i for i in sides if pieces[i][0] == 'black']
sides_l = [i for i in sides if pieces[i][1] == 'black']
sides_d = [i for i in sides if pieces[i][2] == 'black']
sides_r = [i for i in sides if pieces[i][3] == 'black']
inners = [i for i in range(len(pieces)) if black_counts[i] == 0]
print('Corners:', [ul, bl, br, ur])
print('Sides_U:', sides_u)
print('Sides_L:', sides_l)
print('Sides_D:', sides_d)
print('Sides_R:', sides_r)
print('Inner squares:', inners)


# Dynamically fill the board sides, then work our way in
board = [[None for c in range(n)] for r in range(n)]
board[0][0] = ul
board[n-1][0] = bl
board[0][n-1] = ur
board[n-1][n-1] = br
