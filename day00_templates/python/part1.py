#!/usr/bin/env python3

import helper


def main():
    lines = helper.read_lines("example.txt")
    # lines = helper.read_lines("input.txt")
    for line in lines:
        print(line)


##############################################################################

if __name__ == "__main__":
    main()
