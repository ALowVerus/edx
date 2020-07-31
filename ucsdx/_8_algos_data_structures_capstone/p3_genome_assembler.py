# python3
import sys
from heapq import heappush, heappop


class LinkedList:
    def __init__(self, s=None):
        self.left = None
        self.right = None
        self.size = 0
        if s is not None:
            for c in s:
                self.add_right(c)

    def add_left(self, v):
        self.add(v, 'left')

    def add_right(self, v):
        self.add(v, 'right')

    def add(self, v, direction):
        node = LinkedList.Node(v)
        if self.size == 0:
            self.left = node
            self.right = node
        elif direction == 'right':
            self.right.right = node
            node.left = self.right
            self.right = node
        elif direction == 'left':
            self.left.left = node
            node.right = self.left
            self.left = node
        else:
            raise Exception('Cannot add except through right and left.')
        self.size += 1

    def pop_left(self):
        return self.pop('left')

    def pop_right(self):
        return self.pop('right')

    def pop(self, direction):
        if self.size == 0:
            raise Exception('Tried to pop from empty linked list.')
        self.size -= 1
        if direction == 'right':
            node = self.right
            self.right = self.right.left
            if self.right:
                self.right.right = None
            node.left = None
        elif direction == 'left':
            node = self.left
            self.left = self.left.right
            if self.left:
                self.left.left = None
            node.right = None
        else:
            raise Exception("Cannot pop except from right or left.")
        v = node.v
        del node
        return v

    @classmethod
    def merge(cls, a1, a2):
        a1.right.right = a2.left
        a2.left.left = a1.right
        a1.right = a2.right
        a1.size += a2.size
        del a2
        return a1

    def __str__(self):
        node = self.left
        r = []
        while node is not None:
            r.append(node.v)
            node = node.right
        return "[{}]".format(', '.join([str(v) for v in r]))

    class Node:
        def __init__(self, v):
            self.v = v
            self.left = None
            self.right = None


class GenomeKMerCompiler:
    def __init__(self):
        self.adj = {}
        self.in_edges = {}
        self.k = 0

    class ContigLink:
        def __init__(self, target=None):
            self.hash = target
            self.path_chars = LinkedList()
            if target:
                self.path_chars.add_right(target[-1])
            self.counts = LinkedList()
            self.counts_tot = 0

        def __str__(self):
            return "ContigLink | hash: {}, path_chars {}, counts {}, counts_tot {}" \
                .format(self.hash, str(self.path_chars), str(self.counts), self.counts_tot)

        @classmethod
        def merge_each_item_in_a_to_left_of_b(cls, a, b):
            new_a = []
            for a_item in a:
                new_link = GenomeKMerCompiler.ContigLink()
                new_link.hash = b.hash
                new_link.path_chars.left = a_item.path_chars.left
                a_item.path_chars.right.right = b.path_chars.left
                new_link.path_chars.right = b.path_chars.right
                new_link.counts.left = a_item.counts.left
                a_item.counts.right.right = b.counts.left
                new_link.counts.right = b.counts.left
                new_link.counts_tot = a_item.counts_tot + b.counts_tot
                new_a.append(new_link)
            return new_a

    def process_reads(self, reads, k):
        self.k = k
        kmers = []
        for read in reads:
            kmers.extend([read[i:i + k] for i in range(len(read) - k + 1)])
        kmer_edges = [(kmer[:-1], kmer[1:]) for kmer in kmers]
        self.adj = {s: {} for s, t in kmer_edges}
        self.in_edges = {t: {} for s, t in kmer_edges}
        for s, t in kmer_edges:
            self.adj[s][t] = [GenomeKMerCompiler.ContigLink(t)]
            self.adj[s][t][0].counts = 0
            self.in_edges[t][s] = 1
        for s, t in kmer_edges:
            self.adj[s][t][0].counts += 1
        for s in self.adj:
            for t in self.adj[s]:
                count = self.adj[s][t][0].counts
                a = LinkedList()
                a.add_right(count)
                self.adj[s][t][0].counts = a
                self.adj[s][t][0].counts_tot = count

    def simplify_contigs(self, verbose=False):
        # Iterate over a static list of all nodes
        s_options = list(self.adj.keys())
        while s_options:
            source_hash = s_options.pop()
            # If the node is still alive and it is part of a singleton:
            if source_hash in self.adj and \
                    len(self.adj[source_hash]) == 1 and \
                    len(self.adj[source_hash][list(self.adj[source_hash].keys())[0]]) == 1 and \
                    source_hash in self.in_edges and \
                    len(self.in_edges[source_hash]) == 1 and \
                    self.in_edges[source_hash][list(self.in_edges[source_hash].keys())[0]] == 1 and \
                    list(self.in_edges[source_hash].keys())[0] != source_hash:
                # De-link the parent and source
                parent_hash, _ = self.in_edges[source_hash].popitem()
                source_link = self.adj[parent_hash].pop(source_hash)
                source_link = source_link[0]
                # De-link the source and child
                child_hash, child_link = self.adj[source_hash].popitem()
                child_link = child_link[0]
                self.in_edges[child_hash].pop(source_hash)
                # Remove the now-defunct source hash entries
                self.adj.pop(source_hash)
                self.in_edges.pop(source_hash)
                # Re-link the child to the parent
                child_link.path_chars = LinkedList.merge(source_link.path_chars, child_link.path_chars)
                child_link.counts = LinkedList.merge(source_link.counts, child_link.counts)
                child_link.counts_tot = source_link.counts_tot + child_link.counts_tot
                if child_hash not in self.adj[parent_hash]:
                    self.adj[parent_hash][child_hash] = []
                self.adj[parent_hash][child_hash].append(child_link)
                if parent_hash not in self.in_edges[child_hash]:
                    self.in_edges[child_hash][parent_hash] = 0
                self.in_edges[child_hash][parent_hash] += 1

    def print(self):
        print('Printing:')
        print('In-Edges:', self.in_edges)
        for s, conns in self.adj.items():
            print(s, '>>>')
            for t, contigs in conns.items():
                print('\t', t, '>>>')
                for contig in contigs:
                    print('\t\t', str(contig))
        print()
        print()
        print()

    def generate_mapping(self):
        i = 0
        mapping = {}
        adj = {}
        for source in self.adj:
            if source not in mapping:
                mapping[source] = i
                adj[i] = {}
                i += 1
            for target in self.adj[source]:
                if target not in mapping:
                    mapping[target] = i
                    adj[i] = {}
                    i += 1
                adj[mapping[source]][mapping[target]] = []
                for path in self.adj[source][target]:
                    adj[mapping[source]][mapping[target]].append(path.path_chars.size)
        return adj

    def get_sources_and_sinks(self):
        sinks = set()
        sources = set()
        for s in self.adj:
            if s not in self.in_edges and \
                    len(self.adj[s]) == 1 and \
                    len(self.adj[s][list(self.adj[s].keys())[0]]) == 1 and \
                    s != list(self.adj[s].keys())[0]:
                sources.add(s)
            for t in self.adj[s]:
                if t not in self.adj and \
                        len(self.in_edges[t]) == 1 and \
                        self.in_edges[t][list(self.in_edges[t].keys())[0]] == 1:
                    sinks.add(t)
        return sources, sinks

    def unlink_parent_from_child(self, parent, child, link_index):
        self.adj[parent][child].pop(link_index)
        if len(self.adj[parent][child]) == 0:
            self.adj[parent].pop(child)
            if len(self.adj[parent]) == 0:
                self.adj.pop(parent)
        self.in_edges[child][parent] -= 1
        if self.in_edges[child][parent] == 0:
            self.in_edges[child].pop(parent)
            if len(self.in_edges[child]) == 0:
                self.in_edges.pop(child)

    def kill_tips(self, verbose=False):
        sources, sinks = self.get_sources_and_sinks()
        # Iteratively the sources and sinks
        source_tip_count = 0
        sink_tip_count = 0
        while sources or sinks:
            # Kill the sources
            while sources:
                source = sources.pop()
                # self.print()
                # print(source, sources)
                child = list(self.adj[source].keys())[0]
                source_tip_count += self.adj[source][child][0].path_chars.size
                self.unlink_parent_from_child(source, child, 0)
                # If the child is a dead end, mark it a sink
                if child not in self.adj:
                    if child not in self.in_edges:
                        if child in sources:
                            sources.remove(child)
                        if child in sinks:
                            sinks.remove(child)
                    elif len(self.in_edges[child]) == 1 and \
                            self.in_edges[child][list(self.in_edges[child].keys())[0]] == 1:
                        sinks.add(child)
                # If the child has its own children, consider adding it to the queue
                elif child not in self.in_edges and \
                        len(self.adj[child]) == 1 and \
                        len(self.adj[child][list(self.adj[child].keys())[0]]) == 1 and \
                        child != list(self.adj[child].keys())[0]:
                    sources.add(child)
            # Kill the sinks
            while sinks:
                sink = sinks.pop()
                # print(sink, sources, sinks, list(self.adj.keys()), list(self.in_edges.keys()))
                # self.print()
                parent = list(self.in_edges[sink].keys())[0]
                sink_tip_count += self.adj[parent][sink][0].path_chars.size
                self.unlink_parent_from_child(parent, sink, 0)
                # If the parent is now a dead end, add it to the list of sinks
                if parent not in self.adj:
                    if parent not in self.in_edges:
                        if parent in sources:
                            sources.remove(parent)
                        if parent in sinks:
                            sinks.remove(parent)
                    elif len(self.in_edges[parent]) == 1 and \
                            self.in_edges[parent][list(self.in_edges[parent].keys())[0]] == 1:
                        sinks.add(parent)
                # If the parent has more children, consider adding it to the sources
                elif parent not in self.in_edges and \
                        len(self.adj[parent]) == 1 and \
                        len(self.adj[parent][list(self.adj[parent].keys())[0]]) == 1 and \
                        parent != list(self.adj[parent].keys())[0]:
                    sources.add(parent)
        if verbose:
            print(source_tip_count, sink_tip_count)
        return source_tip_count + sink_tip_count

    def count_bubbles(self, bubble_size):
        bubble_paths = set()
        for s in self.adj:
            for t in self.adj[s]:
                if len(self.adj[s][t]) > 1:
                    bubble_paths.add((s, t))
        bubble_count = 0
        while bubble_paths:
            s, t = bubble_paths.pop()
            # Add the bubbles seen at this node to the total bubble count
            bubble_count += len(self.adj[s][t]) - 1
            # Choose the best path by comparing scores, then set the chosen best to the only available path
            best_i = max([i for i in range(len(self.adj[s][t]))], key=lambda j: self.adj[s][t][j].path_chars.size)
            self.in_edges[t][s] = 1
            self.adj[s][t] = [self.adj[s][t][best_i]]
            # Since this path from s to t is now a singleton,
            # all paths from the parent of s to s can be joined to the s-t link.
            # This will condense the paths along s's parent, possibly enabling it to be merged itself.
            while s in self.adj and len(self.adj[s]) == 1 and \
                    s != list(self.adj[s].keys())[0] and \
                    s in self.in_edges and len(self.in_edges[s]) == 1 and \
                    s != list(self.in_edges[s].keys())[0]:
                s_t_path = self.adj[s][t][0]
                p = list(self.in_edges[s].keys())[0]
                p_s_paths = self.adj[p][s]
                self.adj[p].pop(s)
                self.adj.pop(s)
                self.in_edges[s].pop(p)
                self.in_edges[t].pop(s)
                self.in_edges.pop(s)
                if t not in self.adj[p]:
                    self.adj[p][t] = []
                    self.in_edges[t][p] = 0
                self.in_edges[t][p] += len(p_s_paths)
                p_t_paths = GenomeKMerCompiler.ContigLink.merge_each_item_in_a_to_left_of_b(p_s_paths, s_t_path)
                for p_t_path in p_t_paths:
                    self.adj[p][t].append(p_t_path)
                if len(self.adj[p][t]) > 1:
                    bubble_paths.add((p, t))
        return bubble_count


def run(reads, k, t, plan, verbose=False):
    # Generate a compiler
    compiler = GenomeKMerCompiler()
    # Read in the reads
    compiler.process_reads(reads, k)

    if verbose:
        compiler.print()

    # Reduce edges by simplifying to contigs
    compiler.simplify_contigs(verbose=verbose)

    if verbose:
        compiler.print()

    # Extend t spaces out from each edge to find bubbles
    if plan == "finding_bubbles":
        print(compiler.count_bubbles(t))

    # Iteratively kill nodes with no connections
    elif plan == "finding_tips":
        print(compiler.kill_tips(verbose=verbose))
        if verbose:
            print(compiler.get_sources_and_sinks())

    if verbose:
        compiler.print()


from random import choice

testing = False
test_number = 0
plan = "finding_bubbles"

if not testing:
    if plan == "finding_bubbles":
        k, t = map(int, input().split(' '))
        reads = [line.strip() for line in sys.stdin if line.strip()]
    elif plan == "finding_tips":
        reads = [line.strip() for line in sys.stdin if line.strip()]
        k, t = 15, 15
    else:
        raise Exception("Not sure what you're trying te do here.")
    run(reads, k, t, plan, verbose=False)
elif test_number == 0:
    k, t = 4, 4
    reads = [
        "AAAC",
        "AACA",
        "ACAC",
        "CACG",
        "ACGA",
        "AAAT",
        "AATC",
        "ATCC",
        "TCCG",
        "CCGA",
        "AATG",
        "ATGC",
        "TGCG",
        "GCGA",
        "CGAA",
        "GAAA",
    ]
    run(reads, k, t, plan, verbose=True)
else:
    k, t = 8, 8
    read_len = 40
    s_len = 1618
    read_offset = 2
    reads_count = 400
    for j in range(1):
        s = ''.join([choice('ACTG') for i in range(s_len)])
        reads = [s[i:(i + read_len)] + s[:(i + read_len) % s_len if i + read_len > s_len else 0]
                 for i in range(0, s_len, read_offset)]
        reads = list({choice(reads) for i in range(100)})
        print(reads)
        run(reads, k, t, plan, verbose=True)


# hit_failure = True
# while hit_failure:
#     hit_failure = False
#     i = 0
#     while not hit_failure and i < len(reads)-1:
#         try:
#             run(reads[:i] + reads[i + 1:], k, t)
#         except Exception as e:
#             hit_failure = True
#         if hit_failure:
#             reads.pop(i)
#         else:
#             i += 1
# print(reads)
