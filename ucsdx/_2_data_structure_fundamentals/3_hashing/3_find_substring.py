# python3

def read_input():
    return (input().rstrip(), input().rstrip())


def print_occurrences(output):
    print(' '.join(map(str, output)))


def compare_pattern_to_text_at_i(pattern, text, i):
    di = 0
    while di < len(pattern) and text[i + di] == pattern[di]:
        di += 1
    return di == len(pattern)


def get_occurrences_brute(pattern, text):
    res = []
    for i in range(len(text) - len(pattern) + 1):
        if compare_pattern_to_text_at_i(pattern, text, i):
            res.append(i)
    return res


def get_occurrences_distributed(pattern, text):
    alphabet_length = 26
    prime = 10000000003
    current_hash = 0
    pattern_hash = 0
    multiplicand = 1
    for i in range(len(pattern)):
        pattern_hash += (ord(pattern[len(pattern) - i - 1]) - ord('a')) * multiplicand
        pattern_hash %= prime
        current_hash += (ord(text[len(pattern) - i - 1]) - ord('a')) * multiplicand
        current_hash %= prime
        if i != len(pattern) - 1:
            multiplicand *= alphabet_length
            multiplicand %= prime
    max_hash = multiplicand
    hashes = {current_hash: [0]}
    for i in range(1, len(text)-len(pattern)+1):
        current_hash -= max_hash * (ord(text[i-1])-ord('a'))
        current_hash *= alphabet_length
        current_hash += ord(text[i+len(pattern)-1]) - ord('a')
        current_hash %= prime
        if current_hash not in hashes:
            hashes[current_hash] = []
        hashes[current_hash].append(i)
    candidates = hashes[pattern_hash]
    return candidates


def get_occurrences(pattern, text):
    return get_occurrences_distributed(pattern, text)


if __name__ == '__main__':
    print_occurrences(get_occurrences(*read_input()))
