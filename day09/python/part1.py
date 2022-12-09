#!/usr/bin/env python3

import sys

import helper


def signum(n: int):
    if n < 0:
        return -1
    elif n == 0:
        return 0
    else:
        return 1


class Rope:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def touching(self, other: "Rope") -> bool:
        x_dist = abs(self.x - other.x)
        y_dist = abs(self.y - other.y)
        return x_dist <= 1 and y_dist <= 1

    def same_row(self, other: "Rope") -> bool:
        return self.y == other.y

    def same_column(self, other: "Rope") -> bool:
        return self.x == other.x

    def follow(self, other: "Rope") -> None:
        if self.touching(other):
            return  # nothing to do
        # else, not touching
        if self.same_row(other):
            where = other.x - self.x
            self.x += signum(where)
            return  # we're done
        if self.same_column(other):
            where = other.y - self.y
            self.y += signum(where)
            return  # we're done
        # else, we need to move diagonally
        where_x = other.x - self.x
        where_y = other.y - self.y
        self.x += signum(where_x)
        self.y += signum(where_y)


class Area:
    def __init__(self) -> None:
        self.head = Rope(0, 0)
        self.tail = Rope(0, 0)
        self.visited_by_tail: set[tuple[int, int]] = {(self.tail.x, self.tail.y)}

    def head_right(self):
        self.head.x += 1
        self.tail.follow(self.head)
        self.visited_by_tail.add((self.tail.x, self.tail.y))

    def head_left(self):
        self.head.x -= 1
        self.tail.follow(self.head)
        self.visited_by_tail.add((self.tail.x, self.tail.y))

    def head_up(self):
        self.head.y += 1
        self.tail.follow(self.head)
        self.visited_by_tail.add((self.tail.x, self.tail.y))

    def head_down(self):
        self.head.y -= 1
        self.tail.follow(self.head)
        self.visited_by_tail.add((self.tail.x, self.tail.y))

    def show(self):
        return

        rows = 5
        columns = 6
        for y in range(rows)[::-1]:
            for x in range(columns):
                c = "."
                if (x, y) == (self.head.x, self.head.y):
                    c = "H"
                if (x, y) == (self.tail.x, self.tail.y):
                    c = "T"
                sys.stdout.write(c)
            #
            print()
        #
        print("Press Enter to continue...")
        input()


def main():
    # lines = helper.read_lines("example.txt")
    lines = helper.read_lines("input.txt")

    area = Area()
    area.show()

    for line in lines:
        parts = line.split()
        direction, steps = parts[0], int(parts[1])
        for i in range(steps):
            if direction == "R":
                area.head_right()
                area.show()
            if direction == "U":
                area.head_up()
                area.show()
            if direction == "L":
                area.head_left()
                area.show()
            if direction == "D":
                area.head_down()
                area.show()
        #
    #
    result = len(area.visited_by_tail)
    print(result)


##############################################################################

if __name__ == "__main__":
    main()
