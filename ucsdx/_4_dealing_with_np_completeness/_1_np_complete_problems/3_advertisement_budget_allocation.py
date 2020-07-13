# python3
# def generator():
#     from urllib.parse import quote
#     from selenium.webdriver import Chrome
#     from time import sleep
#     import re
#
#     fp = open("../np_complete/output.txt", 'w')
#     driver = Chrome()
#     for a in range(2):
#         for b in range(2):
#             for c in range(2):
#                 for d in range(2):
#                     for e in range(2):
#                         for f in range(2):
#                             for g in range(2):
#                                 for h in range(2):
#                                     line = [a, b, c, d, e, f, g, h]
#                                     if sum(line) != 0 and sum(line) != 8:
#                                         options = ["a0b0c0", "a0b0c1", "a0b1c0", "a0b1c1", "a1b0c0", "a1b0c1", "a1b1c0",
#                                                    "a1b1c1"]
#                                         options = [option for i, option in enumerate(options) if line[i] == 1]
#                                         options = [' & '.join([('~' if part[1] == '0' else '') + part[0] for part in
#                                                                [(option[0:2]), (option[2:4]), (option[4:6])]]) for
#                                                    option in options]
#                                         formula = " | ".join(["({})".format(option) for option in options])
#                                         url = 'https://www.wolframalpha.com/input/?i={}'.format(quote(formula))
#                                         driver.get(url)
#                                         while 'CNF' not in driver.page_source:
#                                             sleep(0.5)
#                                         res = re.findall(r'CNF(.*)', driver.page_source)[0].replace(' | ', '')
#                                         output = "elif res == ({}, {}, {}, {}, {}, {}, {}, {}):\n\t# {}\n\t# {}\n\tpass".format(
#                                             a, b, c, d, e, f, g, h, formula, res)
#                                         print(output)
#                                         fp.write(output + "\n")
#     driver.close()
#     fp.close()
#     """
#     APP NAME: BooleanCNF
#     APPID: 4GX5HA-RXVJUWQ7UQ
#     USAGE TYPE: Personal/Non-commercial Only
#     https://products.wolframalpha.com/docs/WolframAlpha-API-Reference.pdf
#     """


from sys import stdin

# Import the matrix
n, m = list(map(int, stdin.readline().split()))
A = []
for i in range(n):
    A += [list(map(int, stdin.readline().split()))]
b = list(map(int, stdin.readline().split()))


def fail_early():
    print("2 1")
    print("1")
    print("-1")
    exit()


if n == 0 or m == 0:
    print("1 1")
    print("1 -1 0")
    exit()

# Iterate over the matrix to get valid boolean checks
checks = set()
for i in range(1, m + 1):
    checks.add("{} -{}".format(i, i))

for line, tot in zip(A, b):
    # There are only 3 non-zero coefficients per line. Sift them out.
    valid_pairs = [(i, line[i]) for i in range(len(line)) if line[i] != 0]
    # If there are no pairs, you may have a degenerate case.
    if len(valid_pairs) == 0:
        if tot < 0:
            fail_early()
    # If you have at least one valid pair, move ahead!
    elif len(valid_pairs) == 1:
        ((a_i, a_n),) = valid_pairs
        a_i += 1
        a0 = 0 <= tot
        a1 = a_n <= tot
        new_checks = set()
        if not a0:
            new_checks.add('a')
        if not a1:
            new_checks.add('-a')
        for check in new_checks:
            checks.add(check.replace('a', str(a_i)))
    elif len(valid_pairs) == 2:
        ((a_i, a_n), (b_i, b_n)) = valid_pairs
        a_i, b_i = a_i + 1, b_i + 1
        a0b0 = 0 <= tot
        a0b1 = b_n <= tot
        a1b0 = a_n <= tot
        a1b1 = a_n + b_n <= tot
        new_checks = set()
        if not a0b0:
            new_checks.add('a b')
        if not a0b1:
            new_checks.add('a -b')
        if not a1b0:
            new_checks.add('-a b')
        if not a1b1:
            new_checks.add('-a -b')
        for check in new_checks:
            checks.add(check.replace('a', str(a_i)).replace('b', str(b_i)))
    elif len(valid_pairs) == 3:
        ((a_i, a_n), (b_i, b_n), (c_i, c_n)) = valid_pairs
        a_i, b_i, c_i = a_i + 1, b_i + 1, c_i + 1
        a0b0c0 = 0 <= tot
        a0b0c1 = c_n <= tot
        a0b1c0 = b_n <= tot
        a0b1c1 = b_n + c_n <= tot
        a1b0c0 = a_n <= tot
        a1b0c1 = a_n + c_n <= tot
        a1b1c0 = a_n + b_n <= tot
        a1b1c1 = a_n + b_n + c_n <= tot
        new_checks = set()
        if not a0b0c0:
            new_checks.add('a b c')
        if not a0b0c1:
            new_checks.add('a b -c')
        if not a0b1c0:
            new_checks.add('a -b c')
        if not a0b1c1:
            new_checks.add('a -b -c')
        if not a1b0c0:
            new_checks.add('-a b c')
        if not a1b0c1:
            new_checks.add('-a b -c')
        if not a1b1c0:
            new_checks.add('-a -b c')
        if not a1b1c1:
            new_checks.add('-a -b -c')
        for check in new_checks:
            checks.add(check.replace('a', str(a_i)).replace('b', str(b_i)).replace('c', str(c_i)))
    else:
        raise Exception("Failure! Invalid inputs.")

print(len(checks), m)
for check in checks:
    print(check + ' 0')
