import math
from itertools import zip_longest
from typing import List, NamedTuple


class Point(NamedTuple):
    x: int
    y: int


def read_lines(fname: str) -> List[str]:
    with open(fname) as f:
        return f.read().strip().splitlines()


def angle(a: Point, b: Point, c: Point) -> float:
    """
    from https://medium.com/@manivannan_data/find-the-angle-between-three-points-from-2d-using-python-348c513e2cd
    """
    ang = math.degrees(math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0]))
    return ang + 360 if ang < 0 else ang


def grouper(iterable, n, fillvalue=None):
    """
    Collect data into fixed-length chunks:
    grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx

    (from Peter Norvig's pytudes)
    """
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)
