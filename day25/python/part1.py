#!/usr/bin/env python3

import helper
import snafu


def main():
    # lines = helper.read_lines("example.txt")
    lines = helper.read_lines("input.txt")

    total = 0
    for line in lines:
        total += snafu.snafu2decimal(line)
    #
    print(total)
    print("---")
    result = snafu.decimal2snafu(total)
    print(result)


##############################################################################

if __name__ == "__main__":
    main()
