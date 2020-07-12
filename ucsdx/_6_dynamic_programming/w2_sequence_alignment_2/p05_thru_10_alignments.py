# python3
import sys


def align(m, mu, sigma, eps, s, t, alignment):
    # Generate an array
    a = [[[0, 0, 0] for ct in t + '$'] for cs in s + '$']
    # Populate the array with common substring portions
    for si in range(len(s) + 1):
        for ti in range(len(t) + 1):
            # Populate the upper and lower shelves
            if si == 1:
                a[si][ti][1] = a[si - 1][ti][0] - sigma
            elif si > 1:
                options = [a[si - 1][ti][0] - sigma, a[si - 1][ti][1] - eps]
                a[si][ti][1] = min(options) if alignment == 'edit' else max(options)
            if ti == 1:
                a[si][ti][2] = a[si][ti - 1][0] - sigma
            elif ti > 1 and not (alignment == 'overlap' and si == len(s)):
                options = [a[si][ti - 1][0] - sigma, a[si][ti - 1][2] - eps]
                a[si][ti][2] = min(options) if alignment == 'edit' else max(options)
            # Populate the center
            options = [0] if alignment == 'local' or (alignment in {'fitting', 'overlap'} and ti == 0) else []
            if si > 0 and ti > 0:
                options.append(a[si - 1][ti - 1][0] + (m if s[si-1] == t[ti-1] else -mu))
            if ti > 0:
                options.append(a[si][ti][2])
            if si > 0:
                options.append(a[si][ti][1])
            if len(options) == 0:
                options.append(0)
            # print(si, ti, options)
            a[si][ti][0] = min(options) if alignment == 'edit' else max(options)
    # Print the table
    if False:
        print(('m (match reward) = {}, mu (mismatch cost) = {}, \n' +
               'sigma (break start cost) = {}, eps (break extension cost) = {}').format(m, mu, sigma, eps))
        print('tv     s>     ', '  '.join(["{:13}".format(sc) for sc in s]))
        for ti in range(len(t) + 1):
            print(', '.join(["{:>13}".format(str(row[ti])) for row in a]))
            if ti < len(t):
                print(t[ti])
    # Ascend through the array to get the final substring
    if alignment == 'global' or alignment == 'edit' or alignment == 'affine':
        si, ti = len(s), len(t)
    elif alignment == 'local':
        si, ti = max([(si, ti) for si in range(len(s)+1) for ti in range(len(t)+1)],
                     key=lambda p: a[p[0]][p[1]])
    elif alignment == 'fitting':
        si = max(list(range(len(s)+1))[::-1], key=lambda i: a[i][len(t)])
        ti = len(t)
    elif alignment == 'overlap':
        si = len(s)
        ti = max(list(range(len(t)+1))[::-1], key=lambda i: a[len(s)][i])
    else:
        raise Exception('Invalid alignment type.')
    layer = 0
    final_score = a[si][ti][0]
    char_s = []
    char_t = []
    while si > 0 or ti > 0:
        if layer == 0:
            if si > 0 and ti > 0 \
                    and s[si-1] == t[ti-1] \
                    and a[si-1][ti-1][0] + m == a[si][ti][0]:
                char_t.append(t[ti-1])
                char_s.append(s[si-1])
                si -= 1
                ti -= 1
            elif si > 0 and ti > 0 \
                    and s[si-1] != t[ti-1] \
                    and a[si-1][ti-1][0] - mu == a[si][ti][0]:
                char_t.append(t[ti-1])
                char_s.append(s[si-1])
                si -= 1
                ti -= 1
            elif a[si][ti][0] == a[si][ti][1]:
                layer = 1
            elif a[si][ti][0] == a[si][ti][2]:
                layer = 2
        elif layer == 1:
            char_t.append('-')
            char_s.append(s[si - 1])
            if si == 1 or a[si-1][ti][0] - sigma == a[si][ti][1]:
                layer = 0
            si -= 1
        elif layer == 2:
            char_t.append(t[ti - 1])
            char_s.append('-')
            if ti == 1 or a[si][ti-1][0] - sigma == a[si][ti][2]:
                layer = 0
            ti -= 1
        else:
            si = 0
            ti = 0
    s_str = ''.join(char_s[::-1])
    t_str = ''.join(char_t[::-1])
    return '\n'.join([str(final_score), s_str, t_str]) if alignment != 'edit' else str(final_score)


if __name__ == "__main__":
    mode = 'affine'
    if mode == 'edit_distance':
        s, t = [sys.stdin.readline().strip() for _ in range(2)]
        print(align(0, -1, -1, -1, s, t, 'edit'))
    if mode in {'fitting', 'overlap', 'global_search', 'local_search'}:
        m, mu, sigma = map(int, sys.stdin.readline().strip().split())
        s, t = [sys.stdin.readline().strip() for _ in range(2)]
        print(align(m, mu, sigma, sigma, s, t, mode))
    if mode == "affine":
        m, mu, sigma, eps = map(int, sys.stdin.readline().strip().split())
        s, t = [sys.stdin.readline().strip() for _ in range(2)]
        # m, mu, sigma, eps = 1, 3, 2, 1
        # s, t = "GA", "GTTA"
        # m, mu, sigma, eps = 1, 5, 3, 1
        # s, t = "TTT", "TT"
        print(align(m, mu, sigma, eps, s, t, mode))
