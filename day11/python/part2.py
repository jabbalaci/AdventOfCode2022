#!/usr/bin/env python3

import math
from enum import Enum, auto

import helper


class Operation(Enum):
    PLUS = auto()
    MULTIPLY = auto()
    SQUARE = auto()


class Monkey:
    def __init__(self, text: str, parent: "Game") -> None:
        self.parent = parent
        lines = text.splitlines()
        self._id = self.extract_id(lines[0])
        # print("# id:", self._id)
        self.items: list[int] = self.extract_items(lines[1])
        # print("# items:", self.items)
        self.operation: tuple[Operation, int] = self.extract_operation(lines[2])
        # print("# operation:", self.operation)
        self.divisible_by: int = self.extract_last_number(lines[3])
        # print("# divisible_by:", self.divisible_by)
        self.if_true: int = self.extract_last_number(lines[4])
        # print("# if_true:", self.if_true)
        self.if_false: int = self.extract_last_number(lines[5])
        # print("# if_false:", self.if_false)
        # print("---")

    def take_turn(self) -> None:
        for item in self.items:
            value = self.get_new_increased_value(item)
            value = value % self.parent.magic_number  # for this I had to use some help
            if value % self.divisible_by == 0:
                self.parent.throw(self._id, value, self.if_true)
            else:
                self.parent.throw(self._id, value, self.if_false)
            #
        #
        self.items = []  # all items were thrown

    def get_new_increased_value(self, number: int) -> int:
        op, value = self.operation
        if op == Operation.SQUARE:
            return number * number
        elif op == Operation.PLUS:
            return number + value
        else:  # multiply
            return number * value

    def extract_last_number(self, line: str) -> int:
        return int(line.split()[-1])

    def add_item(self, value: int) -> None:
        self.items.append(value)

    def extract_operation(self, line: str) -> tuple[Operation, int]:
        parts = line.split()
        value = parts[-1]
        op = parts[-2]
        if op == "+":
            return (Operation.PLUS, int(value))
        elif op == "*":
            if value == "old":
                return (Operation.SQUARE, 0)  # 0 is a dummy value here
            else:
                return (Operation.MULTIPLY, int(value))
        else:
            assert False  # we should never get here

    def extract_items(self, line: str) -> list[int]:
        right = line.split(":")[-1]
        return [int(number) for number in right.split(", ")]

    def extract_id(self, line: str) -> int:
        return int(line.split()[-1].rstrip(":"))


class Game:
    rounds = 0

    def __init__(self) -> None:
        self.monkeys: list[Monkey] = []
        self.d: dict[int, int] = {}

    def set_magic_number(self) -> None:
        """
        For this I had to use some help.
        """
        result = 1
        for m in self.monkeys:
            result *= m.divisible_by
        #
        self.magic_number = result

    def add(self, text: str) -> None:
        monkey = Monkey(text, self)
        self.monkeys.append(monkey)

    def throw(self, src: int, value: int, dest: int) -> None:
        self.monkeys[dest].add_item(value)
        #
        if src in self.d:
            self.d[src] += 1
        else:
            self.d[src] = 1

    def take_round(self) -> None:
        Game.rounds += 1
        for m in self.monkeys:
            m.take_turn()

    def show(self) -> None:
        print(f"After round {Game.rounds}:")
        for m in self.monkeys:
            print(f"Monkey {m._id}: {m.items}")


def main():
    # content = helper.read("example.txt")
    content = helper.read("input.txt")

    game = Game()

    for monkey in content.split("\n\n"):
        monkey = monkey.strip()
        game.add(monkey)
    #
    game.set_magic_number()

    for i in range(10_000):
        game.take_round()

    # game.show()
    # print(game.d.values())

    result = math.prod(sorted(game.d.values())[-2:])
    print(result)


##############################################################################

if __name__ == "__main__":
    main()
