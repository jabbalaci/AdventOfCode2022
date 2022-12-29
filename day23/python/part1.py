#!/usr/bin/env python3

import sys
from collections import deque
from enum import Enum, auto

import helper
from helper import Point

# DEBUG = True
DEBUG = False

Position = tuple[int, int]


def wait():
    print("---")
    input("Press Enter to continue...")


# ---------------------------------------------------------------------------


class Direction(Enum):
    NOTHING = auto()  # don't move
    NORTH = auto()
    EAST = auto()
    SOUTH = auto()
    WEST = auto()


# ---------------------------------------------------------------------------


class Elf:
    DirectionsQueue = deque([Direction.NORTH, Direction.SOUTH, Direction.WEST, Direction.EAST])

    def __init__(self, i: int, j: int, parent: "Area") -> None:
        self.parent = parent
        self.loc = Point(x=j, y=i)
        self.proposed_direction = Direction.NOTHING  # it may change later
        self.proposed_location = Point(x=j, y=i)

    def __str__(self) -> str:
        return f"{self.loc}: {self.proposed_direction.name}"

    @staticmethod
    def rotate_left() -> None:
        Elf.DirectionsQueue.rotate(-1)

    def get_neighbor_n(self) -> Position:
        x, y = self.loc.x, self.loc.y
        return (x, y - 1)

    def get_neighbor_ne(self) -> Position:
        x, y = self.loc.x, self.loc.y
        return (x + 1, y - 1)

    def get_neighbor_e(self) -> Position:
        x, y = self.loc.x, self.loc.y
        return (x + 1, y)

    def get_neighbor_se(self) -> Position:
        x, y = self.loc.x, self.loc.y
        return (x + 1, y + 1)

    def get_neighbor_s(self) -> Position:
        x, y = self.loc.x, self.loc.y
        return (x, y + 1)

    def get_neighbor_sw(self) -> Position:
        x, y = self.loc.x, self.loc.y
        return (x - 1, y + 1)

    def get_neighbor_w(self) -> Position:
        x, y = self.loc.x, self.loc.y
        return (x - 1, y)

    def get_neighbor_nw(self) -> Position:
        x, y = self.loc.x, self.loc.y
        return (x - 1, y - 1)

    def get_8_neighbors(self) -> list[Position]:
        return [
            self.get_neighbor_n(),
            self.get_neighbor_ne(),
            self.get_neighbor_e(),
            self.get_neighbor_se(),
            self.get_neighbor_s(),
            self.get_neighbor_sw(),
            self.get_neighbor_w(),
            self.get_neighbor_nw(),
        ]

    def are_all_these_positions_free(self, positions: list[Position]) -> bool:
        elves_here: set[Position] = self.parent.get_elves_positions()
        for pos in positions:
            if pos in elves_here:
                return False
            #
        #
        return True

    def can_go_n(self) -> bool:
        p1 = self.get_neighbor_nw()
        p2 = self.get_neighbor_n()
        p3 = self.get_neighbor_ne()
        return self.are_all_these_positions_free([p1, p2, p3])

    def can_go_s(self) -> bool:
        p1 = self.get_neighbor_sw()
        p2 = self.get_neighbor_s()
        p3 = self.get_neighbor_se()
        return self.are_all_these_positions_free([p1, p2, p3])

    def can_go_w(self) -> bool:
        p1 = self.get_neighbor_nw()
        p2 = self.get_neighbor_w()
        p3 = self.get_neighbor_sw()
        return self.are_all_these_positions_free([p1, p2, p3])

    def can_go_e(self) -> bool:
        p1 = self.get_neighbor_ne()
        p2 = self.get_neighbor_e()
        p3 = self.get_neighbor_se()
        return self.are_all_these_positions_free([p1, p2, p3])

    def set_proposed_direction(self, direction: Direction) -> None:
        self.proposed_location = self.loc
        self.proposed_direction = direction
        x, y = self.proposed_location

        if direction == Direction.NORTH:
            self.proposed_location = Point(x=x, y=y - 1)
        elif direction == Direction.SOUTH:
            self.proposed_location = Point(x=x, y=y + 1)
        elif direction == Direction.WEST:
            self.proposed_location = Point(x=x - 1, y=y)
        elif direction == Direction.EAST:
            self.proposed_location = Point(x=x + 1, y=y)
        else:  # if direction == Direction.NOTHING
            pass

    def discover_possible_movement(self) -> None:
        if self.are_all_these_positions_free(self.get_8_neighbors()):
            self.set_proposed_direction(Direction.NOTHING)
            return
        #

        self.set_proposed_direction(Direction.NOTHING)  # default, it may change (thanx Mocsa :))
        stop = False
        for direction in Elf.DirectionsQueue:
            if direction == Direction.NORTH:
                if self.can_go_n():
                    self.set_proposed_direction(Direction.NORTH)
                    stop = True
                #
            elif direction == Direction.SOUTH:
                if self.can_go_s():
                    self.set_proposed_direction(Direction.SOUTH)
                    stop = True
                #
            elif direction == Direction.WEST:
                if self.can_go_w():
                    self.set_proposed_direction(Direction.WEST)
                    stop = True
                #
            else:  # if direction == Direction.EAST
                if self.can_go_e():
                    self.set_proposed_direction(Direction.EAST)
                    stop = True
                #
            #
            if stop:
                break
            #
        #


# ---------------------------------------------------------------------------


class Area:
    def __init__(self, lines: list[str]) -> None:
        self.elves: list[Elf] = []
        for i, line in enumerate(lines):
            for j, c in enumerate(line):
                if c == "#":
                    self.elves.append(Elf(i, j, self))
                #
            #
        #

    def get_elves_positions(self) -> set[Position]:
        return {(elf.loc.x, elf.loc.y) for elf in self.elves}

    def discover_possible_movements(self) -> None:
        for elf in self.elves:
            elf.discover_possible_movement()
        #
        Elf.rotate_left()

    def move_elves(self) -> None:
        d: dict[Position, int] = {}
        for elf in self.elves:
            pos = elf.proposed_location
            if pos not in d:
                d[pos] = 1
            else:
                d[pos] += 1
            #
        #
        for elf in self.elves:
            x, y = elf.proposed_location
            if d[(x, y)] == 1:
                elf.loc = Point(x=x, y=y)
            #
        #

    def count_elves_who_want_to_move(self) -> int:
        return sum(1 for elf in self.elves if elf.proposed_direction != Direction.NOTHING)

    def start(self) -> None:
        for i in range(10):
            self.discover_possible_movements()
            if self.count_elves_who_want_to_move() == 0:
                break
            #
            self.move_elves()
            #
            if DEBUG:
                print(f"End of round {i+1}:")
                print(f"===========")
                self.show_map()
                # self.show_locations()
                print(self.get_result())
                wait()
        #

    def show_map(self) -> None:
        elves_here: set[Position] = self.get_elves_positions()
        for i in range(-2, 12 - 2):
            for j in range(-3, 14 - 3):
                x, y = j, i
                if (x, y) in elves_here:
                    sys.stdout.write("#")
                else:
                    sys.stdout.write(".")
                #
            print()
        #
        print("---")

    def show_locations(self) -> None:
        for elf in self.elves:
            print(elf)
        #
        print("---")

    def get_rectangle_corners(self) -> tuple[Point, Point, Point, Point]:
        xs = [elf.loc.x for elf in self.elves]
        ys = [elf.loc.y for elf in self.elves]
        p1 = Point(x=min(xs), y=min(ys))
        p2 = Point(x=max(xs), y=min(ys))
        p3 = Point(x=min(xs), y=max(ys))
        p4 = Point(x=max(xs), y=max(ys))
        assert p1.x == p3.x
        assert p2.x == p4.x
        assert p1.y == p2.y
        assert p3.y == p4.y
        return p1, p2, p3, p4

    def get_result(self):
        p1, p2, p3, p4 = self.get_rectangle_corners()
        total = 0
        elves_here: set[Position] = self.get_elves_positions()
        for x in range(p1.x, p2.x + 1):
            for y in range(p1.y, p3.y + 1):
                if (x, y) not in elves_here:
                    total += 1
                #
            #
        #
        # print("# x:", p2.x - p1.x + 1)
        # print("# y:", p3.y - p1.y + 1)
        #
        return total


# ---------------------------------------------------------------------------


def main():
    # lines = helper.read_lines("smaller.txt")
    # lines = helper.read_lines("larger.txt")
    lines = helper.read_lines("input.txt")

    area = Area(lines)
    area.start()
    result = area.get_result()
    print(result)


##############################################################################

if __name__ == "__main__":
    main()
