from ucsdx._5_string_processing.data_structures.suffix_tree import SuffixTreeLinear
from itertools import chain

reads = ['AAC', 'ACG', 'GAA', 'GTT', 'TCG']
tree = SuffixTreeLinear(reads)

tree.print_recurse()

for i in range(len(reads)):
    suffix_prefix_matches = tree.match_prefix_to_tree(reads[i])
    print("Matching '{}': \n{}".format(reads[i], suffix_prefix_matches))
