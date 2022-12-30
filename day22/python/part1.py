#!/usr/bin/env python3

import re
import sys
from collections import deque
from enum import Enum
from typing import NamedTuple

import helper
from helper import Point

char = str

DEFAULT_POINT = Point(-1, -1)  # a non-existing point

# ----------------------------------------------------------------------------


class Direction(Enum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3
    MISSING = 4


def opposite(direction: Direction) -> Direction:
    result: Direction
    if direction == Direction.UP:
        result = Direction.DOWN
    elif direction == Direction.RIGHT:
        result = Direction.LEFT
    elif direction == Direction.DOWN:
        result = Direction.UP
    elif direction == Direction.LEFT:
        result = Direction.RIGHT
    else:
        assert False, "Invalid direction"
    #
    return result


def direction2arrow(direction: Direction) -> char:
    result = ""
    if direction == Direction.UP:
        result = "^"
    elif direction == Direction.DOWN:
        result = "v"
    elif direction == Direction.LEFT:
        result = "<"
    elif direction == Direction.RIGHT:
        result = ">"
    else:
        assert False, "Invalid direction"
    #
    return result


# ----------------------------------------------------------------------------


class Instruction(NamedTuple):
    turn: Direction
    steps: int


# ----------------------------------------------------------------------------


class Area:
    def __init__(self, fname: str) -> None:
        content = helper.read(fname)
        part1, part2 = content.split("\n\n")
        self.lines: list[str] = self.process_part1(part1)
        self.instructions: list[Instruction] = self.process_part2(part2.strip())
        self.four_directions = deque(
            [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        )
        self.curr_pos: Point
        self.curr_direction: Direction
        self.d: dict[Point, Direction] = {}  # to keep track of the path

    def pointing(self) -> Direction:
        return self.four_directions[0]

    def turn_right(self):
        self.four_directions.rotate(-1)

    def turn_left(self):
        self.four_directions.rotate(1)

    def process_part1(self, text: str) -> list[str]:
        result: list[str] = []
        lines: list[str] = text.splitlines()
        # longest = max(len(line) for line in lines)
        for line in lines:
            # line = line + (" " * (longest - len(line)))
            result.append(line.rstrip())
        #
        return result

    def process_part2(self, text: str) -> list[Instruction]:
        result: list[Instruction] = []
        li = re.split(r"(L|R)", text)
        first = int(li.pop(0))
        result.append(Instruction(Direction.MISSING, first))
        for i in range(0, len(li), 2):
            value1 = li[i]
            if value1 == "L":
                direction = Direction.LEFT
            elif value1 == "R":
                direction = Direction.RIGHT
            else:
                assert False, "Invalid direction"
            #
            value2 = int(li[i + 1])
            result.append(Instruction(direction, value2))
        #
        return result

    def set_current_position(self, x: int, y: int, direction: Direction):
        p = Point(x=x, y=y)
        self.curr_pos = p
        self.curr_direction = direction
        self.d[p] = direction
        #
        # self.show_map()

    def init_start_position(self) -> None:
        line = self.lines[0]
        for j, c in enumerate(line):
            if c == ".":
                self.set_current_position(x=j, y=0, direction=Direction.RIGHT)
                break
            #
        #

    def get_point(self, x: int, y: int, direction: Direction) -> Point:
        dest_x, dest_y = x, y
        if direction == Direction.RIGHT:
            dest_x += 1
        elif direction == Direction.LEFT:
            dest_x -= 1
        elif direction == Direction.UP:
            dest_y -= 1
        elif direction == Direction.DOWN:
            dest_y += 1
        else:
            assert False, "Invalid direction"
        #
        i, j = dest_y, dest_x
        if (i < 0) or (j < 0):
            raise IndexError
        try:
            c = self.lines[i][j]
            if c == " ":
                raise IndexError
        except IndexError:
            raise
        else:
            return Point(x=dest_x, y=dest_y)

    def get_point_on_opposite_side(self, x: int, y: int, direction: Direction) -> Point:
        """
        Go to the given direction as long as we can.
        """
        dest_x, dest_y = x, y
        last_good = Point(x=dest_x, y=dest_y)
        try:
            while True:
                if direction == Direction.RIGHT:
                    dest_x += 1
                elif direction == Direction.LEFT:
                    dest_x -= 1
                elif direction == Direction.UP:
                    dest_y -= 1
                elif direction == Direction.DOWN:
                    dest_y += 1
                else:
                    assert False, "Invalid direction"
                #
                i, j = dest_y, dest_x
                if (i < 0) or (j < 0):
                    raise IndexError
                try:
                    c = self.lines[i][j]
                    if c == " ":
                        raise IndexError
                except IndexError:
                    raise
                else:
                    last_good = Point(x=dest_x, y=dest_y)
                #
            #
        except IndexError:
            return last_good

    def check_position_at(self, direction: Direction) -> tuple[bool, Point]:
        x, y = self.curr_pos
        try:
            p: Point = self.get_point(x, y, direction)
        except IndexError:
            p: Point = self.get_point_on_opposite_side(x, y, opposite(direction))
        #
        i, j = p.y, p.x
        c = self.lines[i][j]
        if c == "#":
            return False, DEFAULT_POINT
        else:
            return True, p

    def move(self, direction: Direction, steps: int) -> None:
        for i in range(steps):
            ok, dest = self.check_position_at(direction)
            if ok:
                self.set_current_position(x=dest.x, y=dest.y, direction=direction)
            else:
                break
            #
        #

    def start(self) -> None:
        self.init_start_position()
        first = self.instructions[0]
        self.move(Direction.RIGHT, first.steps)
        for inst in self.instructions[1:]:
            turn = inst.turn
            if turn == Direction.LEFT:
                self.turn_left()
            elif turn == Direction.RIGHT:
                self.turn_right()
            else:
                assert False, "Invalid turn"
            self.curr_direction = self.pointing()  # turn to that direction
            self.move(self.pointing(), inst.steps)
        #

    def get_result(self) -> int:
        row = self.curr_pos.y + 1
        column = self.curr_pos.x + 1
        facing = self.curr_direction.value
        result = 1000 * row + 4 * column + facing
        return result

    def show_raw_map(self) -> None:
        for line in self.lines:
            print("'" + line + "'")
        #

    def print_instructions(self) -> None:
        for inst in self.instructions:
            print(inst)
        #

    def show_map(self) -> None:
        for i, line in enumerate(self.lines):
            for j, c in enumerate(line):
                x, y = j, i
                if (x, y) in self.d:
                    value = direction2arrow(self.d[(x, y)])  # type: ignore
                    sys.stdout.write(value)
                else:
                    sys.stdout.write(c)
                #
            #
            print()
        #
        print("---")
        input("Press ENTER to continue...")


# ----------------------------------------------------------------------------


def main():
    # fname = "example.txt"
    fname = "input.txt"

    area = Area(fname)
    area.start()

    # area.show_raw_map()
    # area.print_instructions()
    # area.show_map()

    result = area.get_result()
    print(result)


##############################################################################

if __name__ == "__main__":
    main()
