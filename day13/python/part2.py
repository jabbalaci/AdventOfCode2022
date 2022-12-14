#!/usr/bin/env python3

import functools
from enum import Enum
from typing import Any

import helper


class Order(Enum):
    LESS = -1
    GREATER = 1
    EQUAL = 0


def is_list(x: Any) -> bool:
    return isinstance(x, list)


def is_int(x: Any) -> bool:
    return isinstance(x, int)


def compare(li1: list, li2: list) -> Order:
    assert is_list(li1)
    assert is_list(li2)

    for idx1, left in enumerate(li1):
        try:
            right = li2[idx1]
        except IndexError:
            return Order.GREATER
        #
        if is_int(left) and is_int(right):
            if left < right:
                return Order.LESS
            elif left > right:
                return Order.GREATER
            #
        elif is_list(left) and is_list(right):
            value = compare(left, right)
            if value in (Order.LESS, Order.GREATER):
                return value
            #
        else:  # one is list, the other is int
            if is_int(left):
                left = [left]
            else:  # right is an int
                right = [right]
            #
            value = compare(left, right)
            if value in (Order.LESS, Order.GREATER):
                return value
            #
        #
    #
    if len(li1) < len(li2):
        return Order.LESS
    elif len(li1) > len(li2):
        return Order.GREATER
    else:
        return Order.EQUAL


def my_cmp(li1: list, li2: list) -> int:
    return compare(li1, li2).value


def main():
    # lines = [line for line in helper.read_lines("example.txt") if line]
    lines = [line for line in helper.read_lines("input.txt") if line]

    lines = [eval(line) for line in lines]

    packet1 = [[2]]
    packet2 = [[6]]

    lines.append(packet1)
    lines.append(packet2)

    lines = sorted(lines, key=functools.cmp_to_key(my_cmp))

    idx1 = lines.index(packet1) + 1
    idx2 = lines.index(packet2) + 1

    result = idx1 * idx2
    print(result)


##############################################################################

if __name__ == "__main__":
    main()
