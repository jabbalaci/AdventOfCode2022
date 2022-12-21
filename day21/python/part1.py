#!/usr/bin/env python3

from pprint import pprint

import helper


class MonkeyMath:
    def __init__(self, lines: list[str]) -> None:
        self.d: dict[str, str] = {}
        for line in lines:
            left, right = line.split(":")
            self.d[left] = right.strip()
        #

    def get_num_value_of(self, key: str) -> int:
        value = self.d[key]
        parts = value.split()
        if len(parts) == 1:
            return int(parts[0])
        elif len(parts) == 3:
            a, op, b = parts
            v1 = self.get_num_value_of(a)
            v2 = self.get_num_value_of(b)
            if op == "+":
                return v1 + v2
            elif op == "-":
                return v1 - v2
            elif op == "*":
                return v1 * v2
            elif op == "/":
                return v1 // v2
            else:
                assert False, "Invalid op"
            #
        else:
            assert False, "We should never get here"
        #

    def get_result(self) -> int:
        result = self.get_num_value_of("root")
        return result


def main():
    # lines = helper.read_lines("example.txt")
    lines = helper.read_lines("input.txt")

    mm = MonkeyMath(lines)

    result = mm.get_result()
    print(result)


##############################################################################

if __name__ == "__main__":
    main()
