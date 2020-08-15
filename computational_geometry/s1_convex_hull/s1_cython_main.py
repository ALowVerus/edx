import time
import pyximport; pyximport.install()
from computational_geometry.s1_convex_hull import s1_cython_code


def main():
    start = time.time()
    from random import randint
    points = [(randint(0, 100), randint(0, 100)) for i in range(30)]
    res = s1_cython_code.double_half_hull(points)
    print(res)


if __name__ == "__main__":
    main()
