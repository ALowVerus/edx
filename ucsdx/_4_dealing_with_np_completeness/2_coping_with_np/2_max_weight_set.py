#uses python3
def get_best_party_ever_attendees(boss_to_employees, names_to_fun_values):
    class Person:
        def __init__(self):
            self.name = None
            self.weight = None
            self.children = []
            self.parent = None

    # Generate a proper tree
    people = {name: Person() for name in names_to_fun_values}
    for name, person in people.items():
        person.name = name
        person.weight = names_to_fun_values[name]
    for boss, employees in boss_to_employees.items():
        for employee in employees:
            people[boss].children.append(people[employee])
            people[employee].parent = people[boss]
    root = people[list(people.keys())[0]]
    while root.parent is not None:
        root = root.parent

    # Get the nodes as buckets organized by height
    buckets = [[root]]
    while len(buckets[-1]) > 0:
        new_bucket = []
        for node in buckets[-1]:
            for child in node.children:
                new_bucket.append(child)
        buckets.append(new_bucket)
    buckets.pop()
    # For each index, generate a max including and a max excluding
    total_weights = {}
    for node in buckets[-1]:
        total_weights[id(node)] = (node.weight, 0)
    for bucket in buckets[:-1][::-1]:
        for parent in bucket:
            best_with = parent.weight + sum([total_weights[id(child)][1] for child in parent.children])
            best_without = sum([max(total_weights[id(child)]) for child in parent.children])
            total_weights[id(parent)] = (best_with, best_without)
    # With the optimal weight determined, proceed down the tree to obtain the optimal people
    chosen_items = set()
    for bucket in buckets:
        for child in bucket:
            if (child.parent is None or child.parent.name not in chosen_items) \
                    and total_weights[id(child)][0] > total_weights[id(child)][1]:
                chosen_items.add(child.name)
    return chosen_items


# Grab input data
size = int(input())
weights = {i: w for i, w in enumerate(map(int, input().split()))}
relationships = {}
for i in range(1, size):
    a, b = list(map(int, input().split()))
    if a-1 not in relationships:
        relationships[a-1] = set()
    relationships[a-1].add(b-1)
    if b - 1 not in relationships:
        relationships[b - 1] = set()
    relationships[b-1].add(a-1)


if size == 0:
    print(0)
elif size == 1:
    print(max([weights[0], 0]))
else:
    boss_to_employees = {}

    # BFS to ensure that the tree goes one way and has one head
    seen = {0}
    q = [0]
    while q:
        source = q.pop()
        boss_to_employees[source] = set()
        for child in relationships[source]:
            if child not in seen:
                boss_to_employees[source].add(child)
                seen.add(child)
                q.append(child)

    # for root, children in relationships.items():
    #     if root not in boss_to_employees:
    #         boss_to_employees[root] = set()
    #     for child in children:
    #         if child not in boss_to_employees:
    #             boss_to_employees[child] = set()
    #         if root not in boss_to_employees[child]:
    #             boss_to_employees[root].add(child)

    max_set = get_best_party_ever_attendees(boss_to_employees, weights)
    print(sum([weights[i] for i in max_set]))