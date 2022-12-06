#!/usr/bin/env python3

import helper

SIZE = 14


def process(text: str) -> int:
    for i in range(len(text) - SIZE + 1):
        sub = text[i : i + SIZE]
        if len(sub) == len(set(sub)):
            return i + SIZE
        #
    #
    return -1


def main():
    text = helper.read("input.txt")
    result = process(text)
    print(result)


##############################################################################

if __name__ == "__main__":
    main()
