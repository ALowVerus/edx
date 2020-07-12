# python3
import sys

"""
For more information on BWT in linear time:
https://ocw.mit.edu/courses/mathematics/18-417-introduction-to-computational-molecular-biology-fall-2004/projects/cox_talk.pdf
"""


def anti_bwt(t):
    use_case = "linear"
    if use_case == "quadratic":
        strings = sorted([c for c in t])
        for i in range(len(t)-1):
            strings = sorted(c + s for c, s in zip(t, strings))
        return strings[0][1:] + strings[0][0]
    elif use_case == "linear":
        # Get a sorted side
        counts = {}
        for c in t:
            if c not in counts:
                counts[c] = 0
            counts[c] += 1
        sorted_letters = sorted(list(counts.keys()))
        sorted_t = "".join([c * counts[c] for c in sorted_letters])
        # Label the sorted and unsorted sides with the numberings of their characters
        counts = {c: 0 for c in t}
        labeled_sorted_side = []
        for c in sorted_t:
            labeled_sorted_side.append((c, counts[c]))
            counts[c] += 1
        counts = {c: 0 for c in t}
        labeled_bwt_side = []
        for c in t:
            labeled_bwt_side.append((c, counts[c]))
            counts[c] += 1
        # Convert the sides into a path
        adj = {}
        for t0, t1 in zip(labeled_bwt_side, labeled_sorted_side):
            adj[t0] = t1
        # Follow the path to generate a string
        c, i = sorted_t[0], 0
        path = []
        for j in range(len(t)):
            c, i = adj[(c, i)]
            path.append((c, i))
        # Convert to string
        return ''.join([c for c, i in path])
    else:
        raise Exception("Improper anti-bwt method.")


def bwt(t, use_case='left_sides'):
    if use_case == 'naive':
        rotations = sorted([t[i:] + t[:i] for i in range(len(t))])
        end_chars = [s[-1] for s in rotations]
        return ''.join(end_chars)
    elif use_case == 'left_sides':
        sorted_indices = sorted([i for i in range(0, len(t))], key=lambda i: t[i:])
        end_chars = [t[i-1] for i in sorted_indices]
        return ''.join(end_chars)
    else:
        raise Exception("Improper bwt method.")


if __name__ == '__main__':
    # text = sys.stdin.readline().strip()
    text = "banana$"
    print('Text:\t\t\t', text)
    print('BWT:\t\t\t', bwt(text))
    print('Reversed BWT:\t', anti_bwt(bwt(text)))
