# python3
# Ensure that brackets match correctly.


from collections import namedtuple

Bracket = namedtuple("Bracket", ["char", "position"])


def are_matching(left, right):
    return (left + right) in ["()", "[]", "{}"]


def find_mismatch(text):
    opening_brackets_stack = []
    for i, c in enumerate(text):
        if c in "([{":
            # Process opening bracket, write your code here
            opening_brackets_stack.append(i)
        elif c in ")]}":
            # If there is nothing to match it to, you're screwed
            if len(opening_brackets_stack) == 0:
                return i + 1
            # If the closing term matches the last enqueued opening term, pop
            elif are_matching(text[opening_brackets_stack[-1]], c):
                opening_brackets_stack.pop()
            # If the closing term mismatches the end of the queue, something is wrong
            else:
                return i + 1
    if len(opening_brackets_stack) > 0:
        return opening_brackets_stack[0] + 1
    return "Success"


def main():
    text = input()
    mismatch = find_mismatch(text)
    # Printing answer, write your code here
    print(mismatch)


if __name__ == "__main__":
    main()
