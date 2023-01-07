import math
from itertools import chain, combinations, zip_longest
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int


class Interval(NamedTuple):
    a: Point
    b: Point


def read(fname: str) -> str:
    with open(fname) as f:
        return f.read()


def read_lines(fname: str) -> list[str]:
    with open(fname) as f:
        return f.read().strip().splitlines()


def read_lines_as_ints(fname: str) -> list[int]:
    return [int(s) for s in read_lines(fname)]


def angle(a: Point, b: Point, c: Point) -> float:
    """
    from https://bit.ly/3ZgLmay
    """
    ang = math.degrees(math.atan2(c[1] - b[1], c[0] - b[0]) - math.atan2(a[1] - b[1], a[0] - b[0]))
    return ang + 360 if ang < 0 else ang


def grouper(iterable, n, fillvalue=None):
    """
    Collect data into fixed-length chunks:
    grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx

    (from Peter Norvig's pytudes)
    """
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


def powerset(iterable):
    """
    powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)

    from https://docs.python.org/3/library/itertools.html
    """
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    """
    Merge Overlapping Intervals

    Examples:

    Input: Intervals = [[1, 3], [2, 4], [6, 8], [9, 10]]
    Output: [[1, 4], [6, 8], [9, 10]]

    Input: Intervals = [[6, 8], [1, 9], [2, 4], [4, 7]]
    Output: [[1, 9]]

    from https://www.geeksforgeeks.org/merging-intervals/
    """
    # Sort the array on the basis of start values of intervals.
    intervals.sort()
    stack = []
    # insert first interval into stack
    stack.append(intervals[0])
    for curr in intervals[1:]:
        # Check for overlapping interval,
        # if interval overlap
        if stack[-1][0] <= curr[0] <= stack[-1][-1]:
            stack[-1][-1] = max(stack[-1][-1], curr[-1])
        else:
            stack.append(curr)
        #
    #
    return stack
