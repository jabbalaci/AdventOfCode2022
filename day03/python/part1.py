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

    chars = []
    for line in lines:
        middle = len(line) // 2
        part1, part2 = line[:middle], line[middle:]
        common = list(set(part1).intersection(set(part2)))[0]
        chars.append(common)
    #
    result = sum(char2num(c) for c in chars)
    print(result)


##############################################################################

if __name__ == "__main__":
    main()
