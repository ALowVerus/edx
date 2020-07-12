import sys


def process_text_to_adj(reads):
    adjacency_list = {}
    for read in reads:
        if read[:-1] not in adjacency_list:
            adjacency_list[read[:-1]] = {}
        if read[1:] not in adjacency_list[read[:-1]]:
            adjacency_list[read[:-1]][read[1:]] = 0
        adjacency_list[read[:-1]][read[1:]] += 1
    return adjacency_list





reads = [line.strip() for line in sys.stdin if line.strip()]
adj = process_text_to_adj(reads)
