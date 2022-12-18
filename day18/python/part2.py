#!/usr/bin/env python3

from queue import Queue

import helper

Point3D = tuple[int, int, int]

IntInterval = tuple[int, int]


def touching(p1: Point3D, p2: Point3D) -> bool:
    """
    Are the two cubes direct neighbors?
    """
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    #
    if x1 == x2 and y1 == y2 and abs(z1 - z2) == 1:
        return True
    if x1 == x2 and z1 == z2 and abs(y1 - y2) == 1:
        return True
    if y1 == y2 and z1 == z2 and abs(x1 - x2) == 1:
        return True
    # else
    return False


def get_6_neighbors(p: Point3D) -> list[Point3D]:
    x, y, z = p
    p1 = (x + 1, y, z)
    p2 = (x - 1, y, z)
    p3 = (x, y + 1, z)
    p4 = (x, y - 1, z)
    p5 = (x, y, z + 1)
    p6 = (x, y, z - 1)
    return [p1, p2, p3, p4, p5, p6]


def analyse(droplets: set[Point3D]) -> tuple[IntInterval, IntInterval, IntInterval]:
    """
    Analyse the space where the droplets are located. Expand the x-y-z coordinates by 1 unit,
    making sure that water around the droplets has some space.
    """
    xs = []
    ys = []
    zs = []
    for x, y, z in droplets:
        xs.append(x)
        ys.append(y)
        zs.append(z)
    #
    return ((min(xs) - 1, max(xs) + 1), (min(ys) - 1, max(ys) + 1), (min(zs) - 1, max(zs) + 1))


# ---------------------------------------------------------------------------


class BreadthFirstSearch:
    """
    Start from an air point and "flood" the space, collecting all the air points.
    """

    def __init__(
        self,
        droplets: set[Point3D],
        x_iv: IntInterval,
        y_iv: IntInterval,
        z_iv: IntInterval,
    ) -> None:
        self.droplets = droplets
        self.x_iv = x_iv
        self.y_iv = y_iv
        self.z_iv = z_iv
        self.start_point: Point3D = (x_iv[0], y_iv[0], z_iv[0])
        self.q: Queue[Point3D] = Queue()
        self.q.put(self.start_point)
        self.airs: set[Point3D] = set()  # will be set later

    def get_result(self) -> int:
        total = 0

        for air in self.airs:
            neighbors: list[Point3D] = get_6_neighbors(air)
            for p in neighbors:
                if p in self.droplets:
                    if touching(air, p):
                        total += 1
                    #
                #
            #
        #
        return total

    def is_inside_big_space(self, p: Point3D) -> bool:
        x, y, z = p
        return (
            (self.x_iv[0] <= x <= self.x_iv[1])
            and (self.y_iv[0] <= y <= self.y_iv[1])
            and (self.z_iv[0] <= z <= self.z_iv[1])
        )

    def get_possible_air_neighbors(self, p: Point3D) -> list[Point3D]:
        result: list[Point3D] = []

        points: list[Point3D] = get_6_neighbors(p)
        for p in points:
            # if it's air inside the big space
            if p not in self.droplets and self.is_inside_big_space(p):
                result.append(p)
            #
        #
        return result

    def start(self) -> None:
        visited: set[Point3D] = set()

        while not self.q.empty():
            first: Point3D = self.q.get()
            points: list[Point3D] = self.get_possible_air_neighbors(first)
            for p in points:
                if (p not in visited) and (p not in self.q.queue):
                    self.q.put(p)
                #
            #
            visited.add(first)
        #
        self.airs = visited


# ---------------------------------------------------------------------------


def main():
    # lines = helper.read_lines("example.txt")
    lines = helper.read_lines("input.txt")

    droplets: set[Point3D] = set()

    for line in lines:
        parts = line.split(",")
        a = int(parts[0])
        b = int(parts[1])
        c = int(parts[2])
        droplets.add((a, b, c))
    #
    x_iv, y_iv, z_iv = analyse(droplets)

    bfs = BreadthFirstSearch(droplets, x_iv, y_iv, z_iv)
    bfs.start()
    result = bfs.get_result()
    print(result)


##############################################################################

if __name__ == "__main__":
    main()
