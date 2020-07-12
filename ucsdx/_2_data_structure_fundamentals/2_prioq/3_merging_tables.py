# python3


class Database:
    def __init__(self, row_counts):
        self.row_counts = row_counts
        self.max_row_count = max(row_counts)
        n_tables = len(row_counts)
        self.ranks = [1] * n_tables
        self.parents = list(range(n_tables))

    def merge(self, src, dst):
        src_parent = src
        while self.parents[src_parent] != src_parent:
            src_parent = self.parents[src_parent]
        dst_parent = dst
        while self.parents[dst_parent] != dst_parent:
            dst_parent = self.parents[dst_parent]
        # If the source and destination have the same parent, they are in a linked group.
        if src_parent == dst_parent:
            return False
        # If one component outweighs the other, place the smaller under the greater.
        elif self.ranks[src_parent] > self.ranks[dst_parent]:
            self.parents[dst_parent] = src_parent
            self.row_counts[src_parent] += self.row_counts[dst_parent]
        elif self.ranks[dst_parent] > self.ranks[src_parent]:
            self.parents[src_parent] = dst_parent
            self.row_counts[dst_parent] += self.row_counts[src_parent]
        # If the two components are of matching rank, set one beneath the other and increase the new parent's rank.
        else:
            self.parents[src_parent] = dst_parent
            self.row_counts[dst_parent] += self.row_counts[src_parent]
            self.ranks[dst_parent] += 1
        # update max_row_count with the new maximum table size
        self.max_row_count = max([self.max_row_count, self.row_counts[src_parent], self.row_counts[dst_parent]])
        return True


def main():
    n_tables, n_queries = map(int, input().split())
    counts = list(map(int, input().split()))
    assert len(counts) == n_tables
    db = Database(counts)
    for i in range(n_queries):
        dst, src = map(int, input().split())
        db.merge(dst - 1, src - 1)
        print(db.max_row_count)


if __name__ == "__main__":
    main()
