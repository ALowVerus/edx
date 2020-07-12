# python3
import sys


def kmer_composition(n, s):
    """Computes the k-mer composition of string text

    Args:
        k:          integer length of k-mers to be found
        text:       string to split into a k-mer composition

    Returns:
        a string with each k-mer in text separated by newlines
    """
    return [s[i:i + n] for i in range(len(s) - n + 1)]


if __name__ == "__main__":
    k = int(sys.stdin.readline().strip())
    text = sys.stdin.readline().strip()

    print('\n'.join(kmer_composition(k, text)))
