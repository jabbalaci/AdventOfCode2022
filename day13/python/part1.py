#!/usr/bin/env python3

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


def main():
    # lines = helper.read("example.txt").strip()
    lines = helper.read("input.txt").strip()

    pairs = lines.split("\n\n")

    total = 0
    for idx, pair in enumerate(pairs, start=1):
        left, right = pair.splitlines()
        left = eval(left)
        right = eval(right)
        value = compare(left, right)
        # print(left)
        # print(right)
        # print(value.name)
        if value == Order.LESS:
            total += idx
        #
        # print("---")
        # input("Press ENTER to continue...")
    #
    print(total)


##############################################################################

if __name__ == "__main__":
    main()
