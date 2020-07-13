# python3

def sanitize_adjacency_list(graph):
    # Convert graph keys to integers
    keys_to_integers = {}
    n = 0
    converted_graph = {}
    for s, sub in graph.items():
        if s not in keys_to_integers:
            keys_to_integers[s] = n
            n += 1
        si = keys_to_integers[s]
        if si not in converted_graph:
            converted_graph[si] = {}
        for f, v in sub.items():
            if f not in keys_to_integers:
                keys_to_integers[f] = n
                n += 1
            sf = keys_to_integers[f]
            converted_graph[si][sf] = v
    return keys_to_integers, converted_graph


def reclaim_true_values(keys_to_integers, converted_path):
    integers_to_keys = {val: key for key, val in keys_to_integers.items()}
    return [integers_to_keys[n] for n in converted_path]


"""
Needs to be augmented with associated list and in-order traversal.
"""
from itertools import chain


class SuffixTreeLinear:
    def __init__(self, a):
        # Sanitize the input
        if type(a) == str:
            if '$' in a:
                raise Exception("Character '$' found in a provided string. '$' is reserved here.")
            self.end_char = '$'
            a = [a]
        elif type(a) == list:
            for item in a:
                if '$' in item:
                    raise Exception("Character '$' found in a provided string. '$' is reserved here.")
            self.end_char = '$'
        else:
            raise Exception("Your given input is neither a string nor a list, but a {}.".format(type(a)))
        # Appropriately identify the end_char and use it to define an indexing system for where matches end.
        counts = {}
        for s in a:
            if s not in counts:
                counts[s] = 0
            counts[s] += 1
        self.a = list(counts.keys())
        self.s = list(chain(*[[c for c in s] + [self.end_char + str(i)] for i, s in enumerate(self.a)]))
        self.substring_assignments = []
        target_index = 0
        for c in self.s:
            self.substring_assignments.append(target_index)
            target_index += int(self.end_char in c)

        # Generate a class of nodes for easy tree traversal.
        parent_reference = self

        self.end_point = 0
        self.node_count = 0

        class SuffixNode:
            index = 0

            def __init__(self, indices=None, suffix_link=None):
                self._i0, self._i1 = indices if indices is not None else (None, None)
                self.suffix_link = suffix_link
                self.children = {}
                self.index = parent_reference.node_count
                self.ender_keys = set()
                self.branch_keys = set()
                parent_reference.node_count += 1

            @property
            def i0(self):
                return self._i0

            @property
            def i1(self):
                return self._i1 if self._i1 != '#' else parent_reference.end_point + 1

            @property
            def edge_length(self):
                return self.i1 - self.i0

            def load_child(self, k, v):
                self.children[k] = v
                if parent_reference.end_char in k:
                    self.ender_keys.add(k)
                else:
                    self.branch_keys.add(k)

            @property
            def sub_list(self):
                return parent_reference.s[self.i0:self.i1]

            def __str__(self):
                return str(self.sub_list)

        # Initialize a traversal state object that can be referenced within defined functions
        class TraversalState:
            def __init__(self):
                self.root = SuffixNode(indices=(0, len(parent_reference.s)))
                self.root.suffix_link = self.root
                self.active_point = self.root
                self.active_edge = None
                self.active_length = 0
                self.remaining = 0
                self.total_descents = 0

            @property
            def active_child(self):
                return None if self.active_edge is None \
                               or self.active_edge not in self.active_point.children \
                    else self.active_point.children[self.active_edge]

        state = TraversalState()
        self.root = state.root

        # Account for each character in the string
        for i in range(len(parent_reference.s)):
            self.end_point = i
            # Notice that we must now add a new edge, in some way shape or form
            state.remaining += 1
            # Set the last added inner point to none at the front of each progression.
            last_internal_node_added = None
            # Loop over until remainder hits 0 or we hit an end condition
            done = False
            while state.remaining > 0 and not done:
                # If we are at a node, either enter a leaf or make a new leaf.
                if state.active_length == 0:
                    if parent_reference.s[self.end_point] not in state.active_point.children:
                        temp = SuffixNode(indices=(self.end_point, '#'), suffix_link=state.root)
                        state.active_point.load_child(parent_reference.s[self.end_point], temp)
                        state.active_point = state.active_point.suffix_link
                        state.remaining -= 1
                        state.active_edge = None
                        if state.active_point is state.root and state.remaining > 0:
                            state.active_length = state.remaining - 1
                            state.active_edge = self.s[self.end_point - state.active_length]
                    # If the current char is indeed in the active point, begin to follow.
                    else:
                        state.active_length += 1
                        state.active_edge = self.s[self.end_point]
                        done = True
                # If inside an active edge, attempt to proceed.
                else:
                    # If the next character matches the next character along this edge, follow the edge.
                    if self.s[state.active_child.i0 + state.active_length] == self.s[self.end_point]:
                        state.active_length += 1
                        done = True
                    # If the next character mismatches the current path, make a new node and path.
                    else:
                        # Generate a new fork and a new ender node, and shove the current child down the tree.
                        new_end = SuffixNode(indices=(self.end_point, '#'),
                                             suffix_link=state.root)
                        new_fork = SuffixNode(
                            indices=(state.active_child.i0, state.active_child.i0 + state.active_length),
                            suffix_link=state.root)
                        state.active_child._i0 = state.active_child.i0 + state.active_length
                        new_fork.load_child(self.s[state.active_child.i0], state.active_child)
                        new_fork.load_child(self.s[new_end.i0], new_end)
                        state.active_point.load_child(self.s[new_fork.i0], new_fork)
                        state.remaining -= 1
                        # If not at the root, and thus at a subsidiary node, simply traverse up the suffix links.
                        if state.active_point is not state.root:
                            state.active_point = state.active_point.suffix_link
                        # If at the root, set the active edge and depth to match the remaining required hits
                        if state.active_point is state.root and state.remaining > 0:
                            state.active_length = state.remaining - 1
                            state.active_edge = self.s[self.end_point - state.active_length]
                        # If there was a round before this, set the earlier fork to suffix link to the new fork.
                        if last_internal_node_added is not None:
                            last_internal_node_added.suffix_link = new_fork
                        # Prime the current fork for later suffix linking
                        last_internal_node_added = new_fork
                # After each round, propagate the state down into the tree if needed.
                while state.active_child is not None and state.active_child.edge_length <= state.active_length:
                    state.active_length -= state.active_child.edge_length
                    state.active_point = state.active_child
                    state.active_edge = parent_reference.s[parent_reference.end_point - state.active_length] \
                        if state.active_length != 0 else None

    def get_substrings(self):
        substrings = []

        def recurse(t, indent):
            for k, v in sorted(list(t.children.items()), key=lambda p: p[0]):
                substrings.append(self.s[v.i0:v.i1])
                recurse(v, indent + 1)

        recurse(self.root, 0)
        return substrings

    def print_recurse(self, tab=0):
        print('Recursing over the tree:')

        def recurse(t, indent, c):
            print('  ' * tab, '  ' * indent, c, t.i0, t.i1,
                  "'{}'".format(self.s[t.i0:t.i1] if type(self.s) == str else ''.join(self.s[t.i0:t.i1])),
                  'Node_id={}'.format(t.index),
                  'Suffix_link={}'.format(t.suffix_link.index if t.suffix_link is not None else None),
                  'Ender_keys={}'.format(t.ender_keys))
            for k, v in sorted(list(t.children.items()), key=lambda p: p[0]):
                recurse(v, indent + 1, k)

        recurse(self.root, 0, None)

    def match_prefix_to_tree(self, s, max_error_rate=0, verbose=False):
        if verbose:
            print("Matching s", s)
        longest_ends = {}
        q = [(self.root, 0, 0)]
        max_allowed_errors = int(max_error_rate * len(s)) if max_error_rate < 1 else max_error_rate
        while q:
            node, prefix_i, error_count = q.pop()
            # If not on the top node, mark off all the completed edges
            if error_count < prefix_i and \
                    ((max_error_rate < 1 and error_count <= prefix_i * max_error_rate) or
                     (max_error_rate >= 1 and error_count < max_allowed_errors)):
                if verbose:
                    print('Checking enders for:', str(node), node.ender_keys)
                ending_strings_at_this_i = [int(end_key.replace(self.end_char, '')) for end_key in node.ender_keys]
                for ending_string_index in ending_strings_at_this_i:
                    suffix_root = self.a[ending_string_index]
                    if suffix_root not in longest_ends:
                        longest_ends[suffix_root] = prefix_i
                    elif longest_ends[suffix_root] < prefix_i:
                        longest_ends[suffix_root] = prefix_i
            # Appropriately advance along branches
            if prefix_i < len(s):
                # If we are at our error's limit, only deal with the exact s match
                if error_count == max_allowed_errors and s[prefix_i] in node.children:
                    keys_to_check = [s[prefix_i]]
                elif error_count == max_allowed_errors and s[prefix_i] not in node.children:
                    keys_to_check = []
                # If we have leeway yet, proceed down all allowed paths
                else:
                    keys_to_check = list(node.branch_keys)
                # Convert all keys into their nodes
                children = [node.children[key] for key in keys_to_check]
                # Iterate over nodes to find matches
                for child in children:
                    if verbose:
                        print('\tAdvancing s {} from prefix_i {} along edge {}'
                              .format(s, prefix_i, str(child)))
                    child_list = child.sub_list
                    child_i = 0
                    additional_error_count = 0
                    if verbose:
                        print('\tAttempting to advance.', s[prefix_i + child_i], child_list[child_i])
                    while child_i < len(child_list) and \
                            self.end_char not in child_list[child_i] and \
                            prefix_i + child_i < len(s) and \
                            error_count + additional_error_count <= max_allowed_errors:
                        if verbose:
                            print("\tAdvancing.", prefix_i + child_i, child_i)
                        additional_error_count += int(s[prefix_i + child_i] != child_list[child_i])
                        child_i += 1
                    if verbose:
                        print('\tFinished at prefix_i {} ({}), child_i {} ({})'.format(prefix_i + child_i, s[
                            prefix_i + child_i] if prefix_i + child_i < len(s) else 'OOB',
                                                                                     child_i, child_list[
                                                                                         child_i] if child_i < len(
                                child_list) else 'OOB'))
                    if error_count + additional_error_count <= max_allowed_errors:
                        if child_i < len(child_list) and self.end_char in child_list[child_i] and \
                                ((max_error_rate < 1 and error_count + additional_error_count <=
                                    (prefix_i + child_i) * max_error_rate) or
                                 (max_error_rate >= 1 and error_count + additional_error_count <= max_error_rate)):
                            suffix_root = self.a[int(child_list[child_i].replace(self.end_char, ''))]
                            if suffix_root not in longest_ends:
                                longest_ends[suffix_root] = prefix_i + child_i
                            elif longest_ends[suffix_root] < prefix_i + child_i:
                                longest_ends[suffix_root] = prefix_i + child_i
                        else:
                            q.append((child, prefix_i + child_i, error_count + additional_error_count))
        return longest_ends

    def check_whether_substring_exists_in_tree(self, s, max_error_count=0, verbose=False):
        if verbose:
            print("Matching substring", s)
        q = [(self.root, 0, 0)]
        while q:
            node, si, error_count = q.pop()
            # Appropriately advance along branches
            if si < len(s):
                # If we are at our error's limit, only deal with the exact s match
                if error_count == max_error_count and s[si] in node.children:
                    keys_to_check = [s[si]]
                # If we have leeway yet, proceed down all allowed paths
                else:
                    keys_to_check = list(node.branch_keys)
                # Convert all keys into their nodes
                children = [node.children[key] for key in keys_to_check]
                # Iterate over nodes to find matches
                for child in children:
                    if verbose:
                        print('\tAdvancing s {} from si {} along edge {}'
                              .format(s, si, str(child)))
                    child_list = child.sub_list
                    child_i = 0
                    additional_error_count = 0
                    if verbose:
                        print('\tAttempting to advance.', s[si + child_i], child_list[child_i])
                    while child_i < len(child_list) and \
                            self.end_char not in child_list[child_i] and \
                            si + child_i < len(s) and \
                            error_count + additional_error_count <= max_error_count:
                        if verbose:
                            print("\tAdvancing.", si + child_i, child_i)
                        additional_error_count += int(s[si + child_i] != child_list[child_i])
                        child_i += 1
                    if verbose:
                        print('\tFinished at si {} ({}), child_i {} ({})'.format(si + child_i, s[
                            si + child_i] if si + child_i < len(s) else 'OOB',
                                                                                     child_i, child_list[
                                                                                         child_i] if child_i < len(
                                child_list) else 'OOB'))
                    if si + child_i == len(s) and error_count + additional_error_count <= max_error_count:
                        return True
                    if error_count + additional_error_count <= max_error_count:
                        q.append((child, si + child_i, error_count + additional_error_count))
        return False


# from ucsdx._5_string_processing.data_structures.suffix_tree import SuffixTreeLinear
# from ucsdx._4_dealing_with_np_completeness.utilities.graph_utilites \
#     import sanitize_adjacency_list, reclaim_true_values
# from test import *


def find_max_weight_hamiltonian_cycle(adj):
    keys_to_integers, converted_graph = sanitize_adjacency_list(adj)
    # for k, conns in converted_graph.items():
    #     print(k, conns)
    start = max([node for node in converted_graph], key=lambda n: max([v for k, v in converted_graph[n].items()]))
    # print('Start:', start)
    path = [[start, sorted(list(converted_graph[start].keys()),
                           key=lambda t: converted_graph[start][t])]]
    seen = {path[0][0]}
    while len(path) < len(keys_to_integers) + 1:
        # print(path, seen)
        if len(path) == len(keys_to_integers):
            if path[0][0] in converted_graph[path[-1][0]]:
                path.append(path[0])
            else:
                seen.remove(path.pop()[0])
        elif len(path[-1][1]) == 0:
            seen.remove(path.pop()[0])
        else:
            s, t = path[-1][0], path[-1][1].pop()
            if t not in seen:
                seen.add(t)
                path.append([t, sorted(list(converted_graph[t].keys()),
                                       key=lambda v: converted_graph[t][v])])
    path = [item[0] for item in path]
    path = reclaim_true_values(keys_to_integers, path)
    return path


def graphify_reads(reads, max_error_rate):
    adj = {}
    tree = SuffixTreeLinear(reads)
    for i in range(len(reads)):
        suffix_prefix_matches = tree.match_prefix_to_tree(reads[i],
                                                          max_error_rate=max_error_rate)
        for k, v in suffix_prefix_matches.items():
            if k not in adj:
                adj[k] = {}
            adj[k][reads[i]] = v
    for s in adj:
        if s in adj[s]:
            adj[s].pop(s)
    return adj


def reconstruct_genome_from_reads(reads, max_error_rate):
    # print('Graphifying!')
    adj = graphify_reads(reads, max_error_rate)
    # for k, conns in sorted(list(adj.items()), key=lambda item: item[0]):
    #     print(k, sorted([(v, '{:2}'.format(p)) for v, p in conns.items()],
    #                     key=lambda item: int(item[1]),
    #                     reverse=True))
    # print('Finding a Hamiltonian cycle!')
    path = find_max_weight_hamiltonian_cycle(adj)
    simple_join = ''.join([path[i][:-adj[path[i]][path[i + 1]]] for i in range(len(path) - 1)])
    true_length = len(simple_join)
    # Count the letters found at each location and resolve them into a circular genome
    letter_counts = []
    offset = 0
    for path_index in range(len(path) - 1):
        # print(' ' * offset, path[path_index], offset, adj[path[path_index]][path[path_index + 1]])
        for read_index in range(len(path[path_index])):
            while offset + read_index >= len(letter_counts):
                letter_counts.append({})
            c = path[path_index][read_index]
            if c not in letter_counts[offset + read_index]:
                letter_counts[offset + read_index][c] = 0
            letter_counts[offset + read_index][c] += 1
        # print(letter_counts)
        offset += len(path[path_index]) - adj[path[path_index]][path[path_index + 1]]
    for i in range(0, len(letter_counts) - true_length):
        for c, v in letter_counts[true_length + i].items():
            if c not in letter_counts[i]:
                letter_counts[i][c] = 0
            letter_counts[i][c] += letter_counts[true_length + i][c]
    for i in range(true_length, len(letter_counts)):
        letter_counts.pop()
    # print(letter_counts)
    res = ''.join([max(list(loc_counts.keys()), key=lambda k: loc_counts[k])
                   for loc_counts in letter_counts])
    return res


def reconstruct_genome(reads, has_errors=False):
    if has_errors:
        return reconstruct_genome_from_reads(reads, 2)
    else:
        return reconstruct_genome_from_reads(reads, 0)


def validate(baseline_truth, generated_solution, reads, has_errors):
    if len(baseline_truth) < len(generated_solution):
        test.expect(False, error_message='')
    else:
        print('\tBaseline: ', baseline_truth)
        print('\tGenerated:', generated_solution)
        print('Validate baseline:')
        baseline_tree = SuffixTreeLinear(baseline_truth * 2)
        for read in reads:
            if not baseline_tree.check_whether_substring_exists_in_tree(read, max_error_count=(2 if has_errors else 0)):
                raise Exception(('Read "{}" not found in the baseline string.\n" +'
                                 '"CALL THE ADMINISTRATOR, THE KATA IS WRONG.').format(read))
        generated_tree = SuffixTreeLinear(generated_solution * 2)
        for read in reads:
            if not generated_tree.check_whether_substring_exists_in_tree(read, max_error_count=(2 if has_errors else 0)):
                test.assert_equals(True, False, error_message=('Read "{}" not found in the generated string.\n" +'
                                                               '"CALL THE ADMINISTRATOR, THE KATA IS WRONG.').format(read))


print('Toy test!')
reads = ['AAC', 'ACG', 'GAA', 'GTT', 'TCG']
validate(reconstruct_genome(reads, has_errors=False),
         reconstruct_genome(reads, has_errors=False),
         reads, 0)

from random import choice, randint, shuffle
s_len = 100
read_len = 50
read_offset = 2
test_count = 2
for is_comprehensive in [True, False]:
    for error_prone in [False, True]:
        test.it('error_prone is {}, is_comprehensive is {}.'.format(error_prone, is_comprehensive))
        for test_i in range(test_count):
            s = ''.join([choice('ACTG') for i in range(s_len)])
            print('Testing on string:', s)
            reads = [s[i:(i + read_len)] + s[:(i + read_len) % s_len if i + read_len > s_len else 0]
                     for i in range(0, s_len, read_offset)]
            shuffle(reads)
            if error_prone:
                for i in range(len(reads)):
                    error_loc = randint(0, len(reads[i]) - 1)
                    reads[i] = reads[i][:error_loc] + choice([c for c in 'ACTG' if c != reads[i][error_loc]]) + reads[i][error_loc + 1:]
            if not is_comprehensive:
                reads = [read for read in reads if randint(0, 50) > 30]
            validate(reconstruct_genome(reads, has_errors=error_prone),
                     reconstruct_genome(reads, has_errors=error_prone),
                     reads, has_errors=error_prone)
    exit()
# testing = False
# if testing:
#     error_prone = True
#     print('SMOL TEST!')
#     reads = ['AAC', 'ACG', 'GAA', 'GTT', 'TCG']
#     max_error_rate = 0.00
#     print(reconstruct_genome_from_reads(reads, max_error_rate))
#
#     print('BIG TEST!')
#     from random import choice, randint
#
#     s_len = 100
#     read_len = 50
#     read_offset = 2
#     # s = ''.join([choice('ACTG') for i in range(s_len)])
#     s = 'GGATTGGCCCGACGCTGGCCAGTACCACATCACGAACCCATACTGCTGCGAGCATTCCCTCATCAAACAAAAAGTACTTCAGAGCTAAGTTATACCTTTA'
#     print(s)
#     reads = [s[i:(i + read_len)] + s[:(i + read_len) % s_len if i + read_len > s_len else 0]
#              for i in range(0, s_len, read_offset)]
#     if error_prone:
#         for i in range(len(reads)):
#             error_loc = randint(0, len(reads[i]) - 1)
#             reads[i] = reads[i][:error_loc] + choice([c for c in 'ACTG' if c != reads[i][error_loc]]) + reads[i][error_loc + 1:]
#     # for i, read in enumerate(reads):
#     #     print(' ' * i * read_offset + read)
#     max_error_rate = 2
#     print(reconstruct_genome_from_reads(reads, max_error_rate))
# else:
#     reads = [input() for i in range(1618)]
#     print(reconstruct_genome_from_reads(reads, 2))
