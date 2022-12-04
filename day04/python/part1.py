#!/usr/bin/env python3

import helper


def get_values(text):
    a, b = text.split("-")
    return (int(a), int(b))


def one_contains_other(left, right):
    v1, v2 = get_values(left)
    v3, v4 = get_values(right)
    elf2_in_elf1 = (v1 <= v3) and (v4 <= v2)
    elf1_in_elf2 = (v3 <= v1) and (v2 <= v4)
    return elf2_in_elf1 or elf1_in_elf2


def main():
    # lines = helper.read_lines("example.txt")
    lines = helper.read_lines("input.txt")
    total = 0
    for line in lines:
        left, right = line.split(",")
        if one_contains_other(left, right):
            total += 1
        #
    #
    print(total)


##############################################################################

if __name__ == "__main__":
    main()
