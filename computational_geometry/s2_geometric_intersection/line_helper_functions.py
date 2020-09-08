from random import randint




def generate_line_segments(segment_count, bound):
    return list((lambda f: {tuple(sorted([(f(), f()), (f(), f())]))
                            for i in range(segment_count)})(lambda: randint(0, bound)))
