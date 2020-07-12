# # A Dynamic Programming based Python program for edit
# # distance problem
# def editDistDP(str1, str2, m, n):
#     # Create a table to store results of subproblems
#     dp = [[0 for x in range(n + 1)] for x in range(m + 1)]
#
#     # Fill d[][] in bottom up manner
#     for i in range(m + 1):
#         for j in range(n + 1):
#
#             # If first string is empty, only option is to
#             # insert all characters of second string
#             if i == 0:
#                 dp[i][j] = j  # Min. operations = j
#
#             # If second string is empty, only option is to
#             # remove all characters of second string
#             elif j == 0:
#                 dp[i][j] = i  # Min. operations = i
#
#             # If last characters are same, ignore last char
#             # and recur for remaining string
#             elif str1[i - 1] == str2[j - 1]:
#                 dp[i][j] = dp[i - 1][j - 1]
#
#                 # If last character are different, consider all
#             # possibilities and find minimum
#             else:
#                 dp[i][j] = 1 + min(dp[i][j - 1],  # Insert
#                                    dp[i - 1][j],  # Remove
#                                    dp[i - 1][j - 1])  # Replace
#
#     return dp[m][n]


# Uses python3
def edit_distance(a, b):
    m = [[0 for cb in '.' + b] for ca in '.' + a]
    for ia in range(len(a)):
        m[ia][0] = ia
    for ib in range(len(b)):
        m[0][ib] = ib
    for ia in range(len(a)):
        for ib in range(len(b)):
            if a[ia] == b[ib]:
                m[ia+1][ib+1] = m[ia][ib]
            else:
                options = [m[ia][ib + 1], m[ia + 1][ib], m[ia][ib] + 1]
                m[ia + 1][ib + 1] = min(options)
    return m[len(a)][len(b)]


tests = [
    ('geek', 'gesek'),
    ('cat', 'cut'),
    ('sunday', 'saturday'),
    ('kitten', 'sitting')
]

for a, b in tests:
    print(a, b, edit_distance(a, b))


if __name__ == "__main__":
    print(edit_distance(input(), input()))
