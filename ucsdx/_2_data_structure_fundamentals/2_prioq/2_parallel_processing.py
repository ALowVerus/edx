# python3

from collections import namedtuple
from heapq import heappop, heappush, heapify

AssignedJob = namedtuple("AssignedJob", ["worker", "started_at"])


def assign_jobs(n_workers, jobs):
    h = [(0, i) for i in range(n_workers)]
    heapify(h)
    res = []
    for job in jobs:
        t, worker_i = heappop(h)
        res.append(AssignedJob(worker_i, t))
        heappush(h, (t + job, worker_i))
    return res


def main():
    n_workers, n_jobs = map(int, input().split())
    jobs = list(map(int, input().split()))
    assert len(jobs) == n_jobs

    assigned_jobs = assign_jobs(n_workers, jobs)

    for job in assigned_jobs:
        print(job.worker, job.started_at)


if __name__ == "__main__":
    main()
