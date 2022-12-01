#!/usr/bin/env python3

import helper


def main():
    # lines = helper.read("example.txt").split("\n\n")
    lines = helper.read("input.txt").split("\n\n")

    sums = []
    for batch in lines:
        numbers = [int(line) for line in batch.strip().split("\n")]
        sums.append(sum(numbers))
    #
    sums = sorted(sums, reverse=True)
    print(sum(sums[:3]))


##############################################################################

if __name__ == "__main__":
    main()
