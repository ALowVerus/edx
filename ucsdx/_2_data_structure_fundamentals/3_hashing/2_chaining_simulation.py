# python3
from collections import deque


class Query:

    def __init__(self, query):
        self.type = query[0]
        if self.type == 'check':
            self.ind = int(query[1])
        else:
            self.s = query[1]


class QueryProcessor:
    _multiplier = 263
    _prime = 1000000007

    def __init__(self, bucket_count):
        self.buckets = [deque() for i in range(bucket_count)]

    def _hash_func(self, s):
        ans = 0
        for c in reversed(s):
            ans = (ans * self._multiplier + ord(c)) % self._prime
        return ans % len(self.buckets)

    def write_search_result(self, was_found):
        print('yes' if was_found else 'no')

    def write_chain(self, chain):
        print(' '.join(chain))

    def read_query(self):
        return Query(input().split())

    def process_query(self, query):
        if query.type == "check":
            # use reverse order, because we append strings to the end
            self.write_chain(self.buckets[query.ind])
        else:
            bucket = self.buckets[self._hash_func(query.s)]
            if query.type == 'find':
                self.write_search_result(query.s in bucket)
            elif query.type == 'add':
                if query.s not in bucket:
                    bucket.appendleft(query.s)
            elif query.type == 'del':
                if query.s in bucket:
                    bucket.remove(query.s)
            else:
                raise Exception('Failed Type Exception.')

    def process_queries(self):
        n = int(input())
        for i in range(n):
            self.process_query(self.read_query())


if __name__ == '__main__':
    bucket_count = int(input())
    proc = QueryProcessor(bucket_count)
    proc.process_queries()
