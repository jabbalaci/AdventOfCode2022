#!/usr/bin/env python3

from collections import deque
from typing import Deque, Dict, List, Set

from helper import Point


##########
## Maze ##
##########

class Maze:
    #
    def __init__(self, maze: str) -> None:
        """
        maze is an ASCII drawing of a maze
        '#': wall
        '.': empty cell
        """
        self.maze = maze
        self.lines = tuple(maze.splitlines())    # immutable
        self.empty_cells: List[Point] = self.collect_empty_cells()

    def collect_empty_cells(self) -> List[Point]:
        li = []
        for i, row in enumerate(self.lines):
            for j, col in enumerate(row):
                if col != '#':
                    li.append(Point(x=j, y=i))
                #
            #
        #
        return li

    def debug(self) -> None:
        for line in self.lines:
            print(line)
        print(self.empty_cells)


################
## Pathfinder ##
################

class Pathfinder:
    #
    def __init__(self, maze: Maze) -> None:
        self.maze = maze
        # self.start_point    will be set later
        # self.end_point    will be set later
        self.point_to_dist: Dict[Point, int] = self.init_point_to_dist()

    def init_point_to_dist(self) -> Dict[Point, int]:
        """
        From this we can read the Manhattan-distance of a point
        from the starting point.
        """
        d: Dict[Point, int] = {}
        for p in self.maze.empty_cells:
            d[p] = 0
        #
        return d

    def set_start_point(self, p: Point) -> None:
        self.start_point = p

    def get_start_point(self) -> Point:
        return self.start_point

    def set_end_point(self, p: Point) -> None:
        self.end_point = p

    def get_end_point(self) -> Point:
        return self.end_point

    def show_maze_with_distance_values(self) -> None:
        """
        Take the maze and put the self.point_to_dist
        on it as if the dictionary were a layer.
        """
        for i, row in enumerate(self.maze.lines):
            for j, col in enumerate(row):
                if col == '#':
                    print('#', end="")
                else:
                    p = Point(x=j, y=i)
                    value = self.point_to_dist[p]
                    print(value, end="")
                #
            #
            print()
        #

    def show(self) -> None:
        self.maze.debug()

    def debug_bfs(self, black: List[Point],
                        grey: Deque[Point],
                        white: Set[Point]) -> None:
        print("Black:", black)
        print("Grey:", grey)
        print("White:", white)

    def get_neighbors(self, p: Point) -> List[Point]:
        """
        Get the four neigbors of a point.
        """
        left = Point(x=p.x-1, y=p.y)
        right = Point(x=p.x+1, y=p.y)
        up = Point(x=p.x, y=p.y-1)
        down = Point(x=p.x, y=p.y+1)
        #
        return [left, right, up, down]

    def find_white_neighbors(self, p: Point, whites: Set[Point]) -> List[Point]:
        li = []
        #
        neigbors = self.get_neighbors(p)
        #
        for point in neigbors:
            if point in whites:
                li.append(point)
            #
        #
        return li

    def find_smallest_neighbor(self, p: Point) -> Point:
        neigbors = self.get_neighbors(p)
        valid_neigbors = [nb for nb in neigbors if nb in self.point_to_dist]
        #
        return min(valid_neigbors, key=lambda p: self.point_to_dist[p])

    def find_shortest_path(self) -> List[Point]:
        """
        The cells are marked with their distances from the
        start point. Now reconstruct the shortest path
        from the end point to the starting point.
        At the end the part is reversed to reflect
        the direction from the starting point to the end point.
        """
        li = []
        p = self.end_point

        while True:
            li.append(p)
            dist = self.point_to_dist[p]
            if dist == 0:
                break
            # else:
            p = self.find_smallest_neighbor(p)
        #
        li.reverse()
        return li

    def start_bfs_discovery(self) -> None:
        """
        Discover all cells in a breadth-first manner.
        """
        black: List[Point] = []
        grey: Deque[Point] = deque()
        white: Set[Point] = set(self.maze.empty_cells)
        # begin: init
        white.remove(self.start_point)
        grey.append(self.start_point)
        # end: init
        # self.debug_bfs(black, grey, white)
        # cnt = 0
        while grey or white:    # stop when both of them are empty
            first = grey.popleft()
            black.append(first)
            neighbors = self.find_white_neighbors(first, white)
            for p in neighbors:
                white.remove(p)
                grey.append(p)
                self.point_to_dist[p] = self.point_to_dist[first] + 1
            #
            # cnt += 1
            # if cnt >= 10:
                # break
        # endwhile

        # self.show_maze_with_distance_values()
        # self.debug_bfs(black, grey, white)
