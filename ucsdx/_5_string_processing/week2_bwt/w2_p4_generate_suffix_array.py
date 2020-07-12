# python3
import sys


def build_suffix_array(t):
  """
  Build suffix array of the string text and
  return a list result of the same length as the text
  such that the value result[i] is the index (0-based)
  in text where the i-th lexicographically smallest
  suffix of text starts.
  """
  # Implement this function yourself
  sorted_indices = sorted([i for i in range(0, len(t))], key=lambda i: t[i:])
  return sorted_indices


if __name__ == '__main__':
  text = sys.stdin.readline().strip()
  # text = "GAC$"
  print(" ".join(map(str, build_suffix_array(text))))