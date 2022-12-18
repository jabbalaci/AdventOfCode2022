#!/usr/bin/env python3

import helper

Point3D = tuple[int, int, int]


def touching(p1: Point3D, p2: Point3D) -> bool:
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


def process(d: dict[Point3D, int]) -> dict[Point3D, int]:
    keys = list(d.keys())
    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            k1 = keys[i]
            k2 = keys[j]
            if touching(k1, k2):
                d[k1] -= 1
                d[k2] -= 1
            #
        #
    #
    return d


def main():
    # lines = helper.read_lines("example.txt")
    lines = helper.read_lines("input.txt")

    d: dict[Point3D, int] = {}

    for line in lines:
        parts = line.split(",")
        a = int(parts[0])
        b = int(parts[1])
        c = int(parts[2])
        d[(a, b, c)] = 6
    #
    d = process(d)
    result = sum(d.values())
    print(result)


##############################################################################

if __name__ == "__main__":
    main()
