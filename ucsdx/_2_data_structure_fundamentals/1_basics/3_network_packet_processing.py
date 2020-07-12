# python3

from collections import namedtuple, deque

Request = namedtuple("Request", ["arrived_at", "time_to_process"])
Response = namedtuple("Response", ["was_dropped", "started_at"])


class Buffer:
    def __init__(self, capacity):
        self.capacity = capacity
        self.queue = deque()
        self.time_to_unload_queue = 0

    def process(self, request):
        while len(self.queue) > 0 and self.queue[0] <= request.arrived_at:
            self.queue.popleft()
        if len(self.queue) == self.capacity:
            return Response(True, -1)
        else:
            if len(self.queue) == 0:
                self.time_to_unload_queue = request.arrived_at
            self.time_to_unload_queue += request.time_to_process
            self.queue.append(self.time_to_unload_queue)
            return Response(False, self.time_to_unload_queue - request.time_to_process)


def process_requests(requests, buffer):
    responses = []
    for request in requests:
        responses.append(buffer.process(request))
    return responses


def main():
    buffer_size, n_requests = map(int, input().split())
    requests = []
    for _ in range(n_requests):
        arrived_at, time_to_process = map(int, input().split())
        requests.append(Request(arrived_at, time_to_process))

    buffer = Buffer(buffer_size)
    responses = process_requests(requests, buffer)

    for response in responses:
        print(response.started_at if not response.was_dropped else -1)


if __name__ == "__main__":
    main()
