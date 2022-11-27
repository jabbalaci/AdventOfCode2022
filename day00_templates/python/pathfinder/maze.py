#!/usr/bin/env python3

from helper import Point
from pathfinder import Maze, Pathfinder


def main() -> None:
    drawing = """
#####
#..E#
#...#
#...#
#S#.#
#.#.#
#####
""".strip()
    maze = Maze(drawing)
    #
    pf = Pathfinder(maze)
    # pf.show()
    start = Point(x=1, y=4)
    end = Point(x=3, y=1)
    pf.set_start_point(start)
    pf.set_end_point(end)
    # pf.show_maze_with_distance_values()
    pf.start_bfs_discovery()
    pf.show_maze_with_distance_values()
    path = pf.find_shortest_path()
    print(path)

##############################################################################

if __name__ == "__main__":
    main()
