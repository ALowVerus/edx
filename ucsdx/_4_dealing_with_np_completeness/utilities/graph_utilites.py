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
