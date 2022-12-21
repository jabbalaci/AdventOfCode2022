#!/usr/bin/env python3

from pprint import pprint

import sympy
from sympy.parsing.sympy_parser import parse_expr

import helper

HUMN = "humn"


class MonkeyMath:
    def __init__(self, lines: list[str]) -> None:
        self.raw: dict[str, str] = {}
        for line in lines:
            left, right = line.split(":")
            if left == HUMN:  # skip it
                continue
            #
            self.raw[left] = right.strip()
        #
        self.partially_solved: dict[str, str] = self.solve_partially(self.raw)

    def solve_partially(self, raw: dict[str, str]) -> dict[str, str]:
        d: dict[str, str] = {}
        for key in raw.keys():
            if key == "root":
                d[key] = raw[key]
            else:
                d[key] = self.get_value_of(key)
        #
        return d

    def get_value_of(self, key: str) -> str:
        value = self.raw[key]
        parts = value.split()
        if len(parts) == 1:
            return parts[0]
        elif len(parts) == 3:
            a, op, b = parts
            v1 = HUMN if a == HUMN else self.get_value_of(a)
            v2 = HUMN if b == HUMN else self.get_value_of(b)
            if v1 == HUMN or v2 == HUMN:
                return f"{v1} {op} {v2}"
            elif HUMN in v1:
                return f"({v1}) {op} {v2}"
            elif HUMN in v2:
                return f"{v1} {op} ({v2})"
            else:
                v1 = int(v1)
                v2 = int(v2)
                if op == "+":
                    return str(v1 + v2)
                elif op == "-":
                    return str(v1 - v2)
                elif op == "*":
                    return str(v1 * v2)
                elif op == "/":
                    return str(v1 // v2)
                else:
                    assert False, "Invalid op"
            #
        else:
            assert False, "We should never get here"
        #

    def process_root(self) -> None:
        left, _, right = self.raw["root"].split()
        # print(f"# {left} = {right}")
        equation = "{0} - {1}".format(self.partially_solved[left], self.partially_solved[right])
        print("#", equation)
        print("---")
        p = parse_expr(equation)
        x = sympy.Symbol(HUMN)
        result = sympy.solve(p, x)[0]
        print(result)


def main():
    # lines = helper.read_lines("example.txt")
    lines = helper.read_lines("input.txt")

    mm = MonkeyMath(lines)

    # pprint(mm.raw)
    # print("---")
    # pprint(mm.partially_solved)

    mm.process_root()


##############################################################################

if __name__ == "__main__":
    main()
