#!/usr/bin/env python3

import sys
from dataclasses import dataclass
from enum import Enum, auto

import helper
from helper import Point

char = str


class Material(Enum):
    ROCK = auto()
    AIR = auto()
    SAND = auto()


class Status(Enum):
    REST = auto()
    AIR = auto()


@dataclass
class Elem:
    material: Material
    status: Status


DEFAULT_ELEM = Elem(material=Material.AIR, status=Status.AIR)


class Sand:
    def __init__(self, parent: "Cave") -> None:
        self.parent = parent
        self.d = self.parent.d
        self.x = 500
        self.y = 0

    def can_go_down(self) -> bool:
        dest = Point(x=self.x, y=self.y + 1)
        e: Elem = self.d.get(dest, DEFAULT_ELEM)
        return e == DEFAULT_ELEM

    def go_down(self) -> None:
        self.y += 1

    def can_go_down_left(self) -> bool:
        dest = Point(x=self.x - 1, y=self.y + 1)
        e: Elem = self.d.get(dest, DEFAULT_ELEM)
        return e == DEFAULT_ELEM

    def go_down_left(self) -> None:
        self.x -= 1
        self.y += 1

    def can_go_down_right(self) -> bool:
        dest = Point(x=self.x + 1, y=self.y + 1)
        e: Elem = self.d.get(dest, DEFAULT_ELEM)
        return e == DEFAULT_ELEM

    def go_down_right(self) -> None:
        self.x += 1
        self.y += 1


def to_char(e: Elem) -> char:
    c: char = "?"
    if e.material == Material.ROCK:
        c = "#"
    elif e.material == Material.AIR:
        c = "."
    elif e.material == Material.SAND:
        c = "o"
    #
    return c


class Cave:
    def __init__(self, lines: list[str]) -> None:
        self.d: dict[Point, Elem] = self.build_cave(lines)
        self.lowest_rock_y: int = self.find_lowest_rock()
        self.overflow = False  # set to True if the cave is full of sand

    def find_lowest_rock(self) -> int:
        maxi = -1
        for p in self.d.keys():
            if p.y > maxi:
                maxi = p.y
            #
        #
        return maxi

    def add_line(self, d: dict[Point, Elem], pair: tuple[str, str]) -> None:
        left, right = pair
        left_x, left_y = left.split(",")
        right_x, right_y = right.split(",")
        #
        left_x = int(left_x)
        left_y = int(left_y)
        right_x = int(right_x)
        right_y = int(right_y)
        #
        if left_x == right_x:
            a, b = sorted([left_y, right_y])
            for y in range(a, b + 1):
                d[Point(x=left_x, y=y)] = Elem(material=Material.ROCK, status=Status.REST)
            #
        else:  # if left_y == right_y
            a, b = sorted([left_x, right_x])
            for x in range(a, b + 1):
                d[Point(x=x, y=left_y)] = Elem(material=Material.ROCK, status=Status.REST)
            #
        #

    def build_cave(self, lines: list[str]) -> dict[Point, Elem]:
        d: dict[Point, Elem] = {}

        for line in lines:
            parts = line.split(" -> ")
            pairs = [(parts[i - 1], parts[i]) for i in range(1, len(parts))]
            for pair in pairs:
                self.add_line(d, pair)
            #
        return d

    def start(self) -> None:
        while not self.overflow:
            sand = Sand(self)
            while True:
                if sand.y > self.lowest_rock_y:
                    self.overflow = True
                    return
                #
                if sand.can_go_down():
                    sand.go_down()
                    continue
                #
                if sand.can_go_down_left():
                    sand.go_down_left()
                    continue
                #
                if sand.can_go_down_right():
                    sand.go_down_right()
                    continue
                #
                break
            #
            self.d[Point(x=sand.x, y=sand.y)] = Elem(material=Material.SAND, status=Status.REST)
            # self.show()

    def count_sand_units(self) -> int:
        total = 0
        for v in self.d.values():
            if v.material == Material.SAND:
                total += 1
            #
        #
        return total

    def show(self) -> None:
        for y in range(0, 9 + 3):
            for x in range(492, 503 + 2):
                e: Elem = self.d.get(Point(x, y), DEFAULT_ELEM)
                sys.stdout.write(to_char(e))
            #
            print()
        #
        print("# lowest rock:", self.lowest_rock_y)
        print("---")
        input("Press ENTER to continue...")


def main():
    # lines = helper.read_lines("example.txt")
    lines = helper.read_lines("input.txt")

    cave = Cave(lines)
    cave.start()

    result = cave.count_sand_units()
    print(result)


##############################################################################

if __name__ == "__main__":
    main()
