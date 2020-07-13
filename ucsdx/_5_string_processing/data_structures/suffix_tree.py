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

    def match_prefix_to_tree(self, prefix, max_error_rate=0, verbose=False):
        if verbose:
            print("Matching prefix", prefix)
        longest_ends = {}
        q = [(self.root, 0, 0)]
        max_allowed_errors = int(max_error_rate * len(prefix))
        while q:
            node, i, error_count = q.pop()
            # If not on the top node, mark off all the completed edges
            if i > 0 and error_count <= i * max_error_rate:
                if verbose:
                    print('Checking enders for:', str(node), node.ender_keys)
                ending_strings_at_this_i = [int(end_key.replace(self.end_char, '')) for end_key in node.ender_keys]
                for ending_string_index in ending_strings_at_this_i:
                    longest_ends[self.a[ending_string_index]] = i
            # Appropriately advance along branches
            if i < len(prefix):
                keys_to_check = []
                # If we are at our error's limit, only deal with the exact prefix match
                if error_count == max_allowed_errors:
                    if prefix[i] in node.children:
                        keys_to_check.append(prefix[i])
                # If we have leeway yet, proceed down all paths
                else:
                    keys_to_check = list(node.branch_keys)
                # Convert all keys into their nodes
                children = [node.children[key] for key in keys_to_check]
                # Iterate over nodes to find matches
                for child in children:
                    if verbose:
                        print('\tAdvancing prefix {} from i {} along edge {}'.format(prefix, i, str(child)))
                    s = child.sub_list
                    j = 0
                    additional_error_count = 0
                    if verbose:
                        print('\tAttempting to advance.', prefix[i + j], s[j])
                    while j < len(s) and self.end_char not in s[j] and i + j < len(prefix) and \
                            error_count + additional_error_count <= max_allowed_errors:
                        if verbose:
                            print("\tAdvancing.", i+j, j)
                        additional_error_count += int(prefix[i + j] != s[j])
                        j += 1
                    if verbose:
                        print('\tFinished at i {} ({}), j {} ({})'.format(i+j, prefix[i+j] if i+j < len(prefix) else 'OOB',
                                                                          j, s[j] if j < len(s) else 'OOB'))
                    if error_count + additional_error_count <= max_allowed_errors:
                        if j < len(s) and self.end_char in s[j] and \
                                error_count + additional_error_count <= (i + j) * max_error_rate:
                            longest_ends[self.a[int(s[j].replace(self.end_char, ''))]] = i
                        else:
                            q.append((child, i + j, error_count + additional_error_count))
        return longest_ends


if __name__ == "__main__":
    print('Running SuffixTreeLinear as main!')
    a = ['AAC', 'ABG']
    tree = SuffixTreeLinear(a)
    s = 'BGA'
    # tree.print_recurse()
    suffix_prefix_matches = tree.match_prefix_to_tree(s)
    print("Matching '{}' against {}: \n{}".format(s, a, suffix_prefix_matches))
