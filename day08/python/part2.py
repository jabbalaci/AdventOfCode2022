#!/usr/bin/env python3

import helper


def get_view_distance(value: str, text: str) -> int:
    # value is a char, actually
    total = 0

    for c in text:
        total += 1
        if c >= value:
            break
        #
    #
    return total


def get_distances_before_and_after(line: str, pos: int) -> tuple[int, int]:
    value = line[pos]
    before = line[:pos]
    after = line[pos + 1 :]
    dist1 = get_view_distance(value, after)
    dist2 = get_view_distance(value, before[::-1])
    return dist1, dist2


def get_score(lines: list[str], i: int, j: int) -> int:
    last_row_idx = len(lines) - 1
    last_column_idx = len(lines[0]) - 1
    if i == 0 or i == last_row_idx:
        return 0
    if j == 0 or j == last_column_idx:
        return 0
    # else, if it's inside
    row = lines[i]
    dist1, dist2 = get_distances_before_and_after(row, j)
    column = "".join([line[j] for line in lines])
    dist3, dist4 = get_distances_before_and_after(column, i)
    #
    return dist1 * dist2 * dist3 * dist4


def highest_score(lines: list[str]) -> int:
    scores: list[int] = []
    for row_idx, row in enumerate(lines):
        for column_idx, value in enumerate(row):
            score = get_score(lines, row_idx, column_idx)
            scores.append(score)
            #
        #
    #
    return max(scores)


def main():
    # lines = helper.read_lines("example.txt")
    lines = helper.read_lines("input.txt")

    result = highest_score(lines)
    print(result)


##############################################################################

if __name__ == "__main__":
    main()
