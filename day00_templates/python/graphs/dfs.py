#!/usr/bin/env python3

"""
depth-first search
"""

import copy
from collections import namedtuple
from enum import Enum, auto
from queue import LifoQueue
from typing import NamedTuple, Optional

import helper

char = str


class Direction(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()


class Point(NamedTuple):
    row: int
    col: int


NOT_FOUND = Point(-1, -1)


class Path:
    def __init__(self, points: list[Point]) -> None:
        # self.points: list[Point] = copy.copy(points)
        self.points: list[Point] = points
        self._points_set: set[Point] = set(self.points)

    def get_last_point(self) -> Point:
        return self.points[-1]

    def already_visited(self, p: Point) -> bool:
        return p in self._points_set

    def __len__(self) -> int:
        return len(self.points)

    def __str__(self) -> str:
        return str(self.points)


# ---------------------------------------------------------------------------


class Maze:
    def __init__(self, lines: list[str]) -> None:
        self.lines: list[str] = lines
        self.start_point = self.find_point("S")
        self.end_point = self.find_point("E")

    def find_point(self, c: char) -> Point:
        for row_idx, row in enumerate(self.lines):
            for col_idx, col in enumerate(row):
                if col == c:
                    return Point(row=row_idx, col=col_idx)
                #
            #
        #
        return NOT_FOUND  # we should never get here

    def get_value_of(self, p: Point) -> char:
        result = self.lines[p.row][p.col]
        if result == "S":
            result = "a"
        if result == "E":
            result = "z"
        return result

    def get_point(self, direction: Direction, p: Point) -> Optional[Point]:
        row, col = p.row, p.col
        if direction == Direction.UP:
            row -= 1
        elif direction == Direction.DOWN:
            row += 1
        elif direction == Direction.LEFT:
            col -= 1
        else:  # if direction == Direction.RIGHT:
            col += 1
        #
        if (0 <= row < len(self.lines)) and (0 <= col < len(self.lines[0])):
            return Point(row=row, col=col)
        else:
            return None

    def get_4_points(self, last_point: Point) -> list[Point]:
        points: list[Point | None] = [
            self.get_point(Direction.UP, last_point),
            self.get_point(Direction.DOWN, last_point),
            self.get_point(Direction.LEFT, last_point),
            self.get_point(Direction.RIGHT, last_point),
        ]

        return [p for p in points if p]

    def is_elevation_ok(self, last_point: Point, p: Point) -> bool:
        last_value = self.get_value_of(last_point)
        p_value = self.get_value_of(p)
        return ord(p_value) - ord(last_value) <= 1

    def get_possible_directions(self, path: Path) -> list[Point]:
        last_point = path.get_last_point()
        # up
        points: list[Point] = self.get_4_points(last_point)
        points = [p for p in points if self.is_elevation_ok(last_point, p)]
        points = [p for p in points if path.already_visited(p) == False]

        return points


# ---------------------------------------------------------------------------


class Pathfinder:
    def __init__(self, maze: Maze) -> None:
        self.maze: Maze = maze
        self.q: LifoQueue[Path] = LifoQueue()
        path = Path([self.maze.start_point])
        self.q.put(path)
        self.shortest_path = None  # will be set later

    def reached_end_point(self, path: Path) -> bool:
        return path.get_last_point() == self.maze.end_point

    def start(self) -> None:
        while not self.q.empty():
            first: Path = self.q.get()
            if self.reached_end_point(first):
                if not self.shortest_path:
                    self.shortest_path = first
                    print("# shortest path:", len(self.shortest_path))
                else:
                    if len(first) < len(self.shortest_path):
                        self.shortest_path = first
                        print("# shortest path:", len(self.shortest_path))
                    #
                #
                # print("# a possible solution:", first)
            #
            directions: list[Point] = self.maze.get_possible_directions(first)
            for p in directions:
                path = Path(first.points + [p])
                self.q.put(path)

            # print("# point:", first.get_last_point())
            # print("# to:", directions)
            # print("---")
            # input("Press Enter to continue...")
        #


# ---------------------------------------------------------------------------


def main():
    # lines: list[str] = helper.read_lines("example.txt")
    lines: list[str] = helper.read_lines("input.txt")

    maze = Maze(lines)

    pf = Pathfinder(maze)
    pf.start()

    result = len(pf.shortest_path) - 1  # type: ignore
    print(result)


##############################################################################

if __name__ == "__main__":
    main()
