#!/usr/bin/env python3

import helper

SIZE = 4


def process(text: str) -> int:
    for i in range(len(text) - SIZE + 1):
        sub = text[i : i + SIZE]
        if len(sub) == len(set(sub)):
            return i + SIZE
        #
    #
    return -1


def main():
    ex1 = "mjqjpqmgbljsphdztnvjfqwrcgsmlb"  # 7
    ex2 = "bvwbjplbgvbhsrlpgdmjqwftvncz"  # 5
    ex3 = "nppdvjthqldpwncqszvftbrmjlhg"  # 6
    ex4 = "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg"  # 10
    ex5 = "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw"  # 11

    text = helper.read("input.txt")
    result = process(text)
    print(result)


##############################################################################

if __name__ == "__main__":
    main()
