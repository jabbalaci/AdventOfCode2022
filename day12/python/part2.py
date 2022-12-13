#!/usr/bin/env python3

"""
with Dijkstra's algorithm

Part 2 was very slow. It took 2.5 hours to complete...
"""

import pprint
import sys
from dataclasses import dataclass
from enum import Enum, auto
from typing import NamedTuple, Optional

import helper

char = str

# ---------------------------------------------------------------------------


class Direction(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()


# ---------------------------------------------------------------------------


class Point(NamedTuple):
    row: int
    col: int


NOT_FOUND = Point(-1, -1)

# ---------------------------------------------------------------------------


@dataclass
class Entry:
    node: Point
    dist_from_start: int
    prev_node: Point


# ---------------------------------------------------------------------------


class Path:
    def __init__(self, points: list[Point]) -> None:
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
        self.end_point: Point = self.find_point("E")
        self.lowest_points: list[Point] = self.collect_lowest_points()
        # self.lowest_points.sort(key=self.sort_by_dist_from_end_point)

    def sort_by_dist_from_end_point(self, p: Point) -> int:
        """
        Sort the points by their Manhattan distance from the end point.

        It also works without sorting.
        """
        diff_row = abs(self.end_point.row - p.row)
        diff_col = abs(self.end_point.col - p.col)
        return diff_row + diff_col

    def collect_lowest_points(self) -> list[Point]:
        result: list[Point] = []
        for row_idx, row in enumerate(self.lines):
            for col_idx, col in enumerate(row):
                if col in ("a", "S"):
                    result.append(Point(row=row_idx, col=col_idx))
                #
            #
        #
        return result

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

    def get_possible_directions(self, curr_point: Point) -> list[Point]:
        points: list[Point] = self.get_4_points(curr_point)
        points = [p for p in points if self.is_elevation_ok(curr_point, p)]

        return points

    def get_all_points(self) -> set[Point]:
        rows = len(self.lines)
        cols = len(self.lines[0])

        result: set[Point] = set()
        for row_idx in range(rows):
            for col_idx in range(cols):
                result.add(Point(row=row_idx, col=col_idx))
            #
        #
        return result


# ---------------------------------------------------------------------------


class Pathfinder:
    def __init__(self, maze: Maze, start_point: Point) -> None:
        self.maze: Maze = maze
        self.start_node: Point = start_point
        self.end_node: Point = self.maze.end_point
        self.visited: set[Point] = set()
        self.unvisited: set[Point] = self.maze.get_all_points()
        self.table: dict[Point, Entry] = self.init_table()

    def init_table(self) -> dict[Point, Entry]:
        d: dict[Point, Entry] = {}
        for p in self.unvisited:
            d[p] = Entry(node=p, dist_from_start=sys.maxsize, prev_node=NOT_FOUND)
        #
        d[self.start_node].dist_from_start = 0
        #
        return d

    def reached_end_point(self, path: Path) -> bool:
        return path.get_last_point() == self.maze.end_point

    def start(self) -> None:
        while len(self.unvisited) > 0:  # not empty
            entry: Entry = sorted(
                [self.table[k] for k in self.unvisited], key=lambda e: e.dist_from_start
            )[0]
            directions: list[Point] = self.maze.get_possible_directions(entry.node)
            unvisited_neighbors: set[Point] = self.unvisited.intersection(directions)
            current_value: int = entry.dist_from_start
            for nb in unvisited_neighbors:
                nb_entry: Entry = self.table[nb]
                nb_distance = 1
                nb_new_value: int = current_value + nb_distance
                if nb_new_value < nb_entry.dist_from_start:
                    nb_entry.dist_from_start = nb_new_value
                    nb_entry.prev_node = entry.node
                #
            #
            self.unvisited.remove(entry.node)
            self.visited.add(entry.node)

            # self.show()
        #

    def show(self) -> None:
        pprint.pprint(self.table)
        print("# visited:", self.visited)
        print("# unvisited:", self.unvisited)
        print("---")
        input("Press ENTER to continue...")


# ---------------------------------------------------------------------------


def main():
    # lines: list[str] = helper.read_lines("example.txt")
    lines: list[str] = helper.read_lines("input.txt")

    maze = Maze(lines)

    distances: list[int] = []
    for idx, start_point in enumerate(maze.lowest_points):
        pf = Pathfinder(maze, start_point)
        pf.start()

        # print(pf.table[pf.end_node])
        result = pf.table[pf.end_node].dist_from_start
        print(f"# {idx+1} of {len(maze.lowest_points)} ({start_point}): {result}")
        distances.append(result)
    #
    print("---")
    result = min(distances)
    print(result)


##############################################################################

if __name__ == "__main__":
    main()
