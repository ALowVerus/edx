#python3
import sys


def LCS(s,t):
    # Generate an array
    a = [[0 for ct in t] for cs in s]
    # Populate the array with common substring portions
    for si in range(len(s)):
        for ti in range(len(t)):
            options = [0]
            if si > 0:
                options.append(a[si - 1][ti])
            if ti > 0:
                options.append(a[si][ti - 1])
            options.append((a[si - 1][ti - 1] if si > 0 and ti > 0 else 0) + int(s[si] == t[ti]))
            a[si][ti] = max(options)
    # # Print the table
    # print(' ', ', '.join(["{:>3}".format(tc) for tc in t]))
    # for si in range(len(s)):
    #     print(s[si], ', '.join(["{:3}".format(item) for item in a[si]]))
    # Ascend through the array to get the final substring
    si, ti = len(s) - 1, len(t) - 1
    chars = []
    while si >= 0 and ti >= 0:
        if s[si] == t[ti]:
            chars.append(s[si])
            si -= 1
            ti -= 1
        elif si > 0 and a[si-1][ti] == a[si][ti]:
            si -= 1
        elif ti > 0 and a[si][ti-1] == a[si][ti]:
            ti -= 1
        else:
            si -= 1
            ti -= 1
    return ''.join(chars[::-1])


# test_cases = [
#     ['GACT', 'ATG', 'AT'],
#     ['ACGTCCAGC', 'CGTGC', 'CGTGC'],
# ]
# for s, t, r in test_cases:
#     b = LCS(t, s)
#     print(b == r, b, r)


if __name__ == "__main__":
    s,t = sys.stdin.read().strip().splitlines()
    print(LCS(s,t))
