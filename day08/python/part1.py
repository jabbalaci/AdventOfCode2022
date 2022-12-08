#!/usr/bin/env python3

import helper


def visible_in_line(line: str, pos: int) -> bool:
    value = line[pos]
    before = line[:pos]
    after = line[pos + 1 :]
    return all([c < value for c in before]) or all([c < value for c in after])


def visible(lines: list[str], i: int, j: int) -> bool:
    last_row_idx = len(lines) - 1
    last_column_idx = len(lines[0]) - 1
    if i == 0 or i == last_row_idx:
        return True
    if j == 0 or j == last_column_idx:
        return True
    # else, if it's inside
    row = lines[i]
    if visible_in_line(row, j):
        return True
    column = "".join([line[j] for line in lines])
    if visible_in_line(column, i):
        return True
    #
    return False


def number_of_visible_trees(lines: list[str]) -> int:
    total = 0
    for row_idx, row in enumerate(lines):
        for column_idx, value in enumerate(row):
            if visible(lines, row_idx, column_idx):
                total += 1
            #
        #
    #
    return total


def main():
    # lines = helper.read_lines("example.txt")
    lines = helper.read_lines("input.txt")

    result = number_of_visible_trees(lines)
    print(result)


##############################################################################

if __name__ == "__main__":
    main()
