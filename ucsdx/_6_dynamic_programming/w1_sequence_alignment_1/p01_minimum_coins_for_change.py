#python3
import sys


def find_change(money, coins):
    # TODO: your code here
    history = [0]
    for i in range(1, money+1):
        history.append(-1)
        for coin in coins:
            if i - coin >= 0:
                new_res = history[i - coin] + 1
                history[-1] = new_res if history[-1] == -1 or new_res < history[-1] else history[-1]
    return history[-1]


# test_cases = [
#     [[1, 5], 7, 3],
#     [[1, 2, 3, 4, 5, 10], 10, 1],
#     [[1, 5], 11, 3],
#     [[9, 6, 1], 12, 2],
# ]
#
# for coins, money, correct_output in test_cases:
#     print(find_change(money, coins) == correct_output)


if __name__ == "__main__":
    money = int(sys.stdin.readline().strip())
    coins = list(map(int, sys.stdin.readline().strip().split(',')))
    print(find_change(money, coins))

