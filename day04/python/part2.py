#!/usr/bin/env python3

import helper


def get_values(text):
    a, b = text.split("-")
    return (int(a), int(b))


def overlap(left, right):
    v1, v2 = get_values(left)
    v3, v4 = get_values(right)
    case1 = v1 <= v3 <= v2 <= v4
    case2 = v3 <= v1 <= v4 <= v2
    case3 = v3 <= v1 <= v2 <= v4
    case4 = v1 <= v3 <= v4 <= v2
    return case1 or case2 or case3 or case4


def main():
    # lines = helper.read_lines("example.txt")
    lines = helper.read_lines("input.txt")
    total = 0
    for line in lines:
        left, right = line.split(",")
        if overlap(left, right):
            total += 1
        #
    #
    print(total)


##############################################################################

if __name__ == "__main__":
    main()
