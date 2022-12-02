#!/usr/bin/env python3

import helper

SCORES = {
    "A": 1,
    "B": 2,
    "C": 3,
}

WINNER_CONFIGS = [("A", "B"), ("B", "C"), ("C", "A")]

TO_WIN = dict(WINNER_CONFIGS)

TO_LOSE = {
    "A": "C",
    "B": "A",
    "C": "B",
}


def pre_process(lines: list[str]) -> list[tuple[str, str]]:
    result: list[tuple[str, str]] = []
    for line in lines:
        opponent, me = line.split()
        if me == "X":
            me = TO_LOSE[opponent]
        elif me == "Y":
            me = opponent
        else:
            me = TO_WIN[opponent]
        #
        result.append((opponent, me))
    #
    return result


def evaluate(pair: tuple[str, str]) -> int:
    a, b = pair
    result = 0
    result += SCORES[b]
    if a == b:
        result += 3  # draw
    elif pair in WINNER_CONFIGS:
        result += 6  # win
    else:
        pass  # result += 0
    #
    return result


def main():
    # lines = helper.read_lines("example.txt")
    lines = helper.read_lines("input.txt")

    pairs = pre_process(lines)

    result = 0
    for pair in pairs:
        result += evaluate(pair)
    #
    print(result)


##############################################################################

if __name__ == "__main__":
    main()
