#!/usr/bin/env python3

import helper


def char2num(c: str) -> int:
    if c.islower():
        return ord(c) - ord("a") + 1
    elif c.isupper():
        return 26 + char2num(c.lower())
    else:
        assert False  # we should never get here


def main():
    # lines = helper.read_lines("example.txt")
    lines = helper.read_lines("input.txt")

    total = 0
    for three in helper.grouper(lines, 3):
        a, b, c = three  # type: ignore
        common = list(set(a).intersection(set(b)).intersection(set(c)))[0]
        total += char2num(common)
    #
    print(total)


##############################################################################

if __name__ == "__main__":
    main()
