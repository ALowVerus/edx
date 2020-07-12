from computational_geometry.s2_geometric_intersection.line_helper_functions import LEEWAY


class SegmentEventHeap:
    def __init__(self):
        self.entries = []
        self.hashed_values = set()

    def step(self):
        if len(self.entries) == 0:
            raise Exception("Attempting to pop from an empty heap.")
        target_x = self.entries[0][0]
        popped_points = []
        hits_vertical = False
        while len(self.entries) > 0 and self.entries[0][0] - LEEWAY < target_x < self.entries[0][0] + LEEWAY:
            next_event = self.pop()
            if next_event[1] is None:
                hits_vertical = True
            else:
                popped_points.append(next_event)
        return popped_points, hits_vertical

    def add(self, t, v):
        new_value = (v if t == "Point" else (v, None))
        print("Adding:", new_value)
        if new_value not in self.hashed_values:
            self.hashed_values.add(new_value)
            self.entries.append(new_value)
            self.resolve(len(self.entries) - 1)

    def pop(self):
        # If there are no entries, raise an exception
        if len(self.entries) == 0:
            raise Exception("You've attempted to pop from an empty heap.")
        # If there are any entries, resolve the None downwards
        output, self.entries[0] = self.entries[0], None
        i_parent = 0
        found_rock_bottom = False
        while not found_rock_bottom:
            i_child0 = i_parent * 2 + 1
            i_child1 = i_parent * 2 + 2
            if i_child0 >= len(self.entries):
                found_rock_bottom = True
            elif i_child1 == len(self.entries):
                self.swap(i_child0, i_parent)
                i_parent = i_child0
            elif self.cmp(i_child0, i_child1) > 0:
                self.swap(i_child1, i_parent)
                i_parent = i_child1
            else:
                self.swap(i_child0, i_parent)
                i_parent = i_child0
        # If the None is in the last location, just pop it
        if i_parent == len(self.entries) - 1:
            self.entries.pop()
        # If the None is not in the last location, pop the last item and resolve it upwards from the None spot
        else:
            self.entries[i_parent] = self.entries.pop()
            self.resolve(i_parent)
        self.hashed_values.remove(output)
        return output

    def resolve(self, i):
        child_i = i
        father_i = (child_i + 1) // 2 - 1
        while father_i >= 0 and self.cmp(father_i, child_i) == 1:
            self.swap(child_i, father_i)
            child_i = father_i
            father_i = (child_i + 1) // 2 - 1

    def swap(self, i0, i1):
        self.entries[i0], self.entries[i1] = self.entries[i1], self.entries[i0]

    def cmp(self, i0, i1):
        xs = [self.entries[i][0] for i in [i0, i1]]
        return 1 if xs[0] > xs[1] else -1 if xs[0] < xs[1] else 0