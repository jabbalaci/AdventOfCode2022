#!/usr/bin/env python3

from typing import Optional

import helper
from helper import Interval, Point


class Sensor:
    def __init__(self, line: str, parent: "Area") -> None:
        self.parent = parent
        parts = line.split()
        x = self.parse(parts[2])
        y = self.parse(parts[3])
        beacon_x = self.parse(parts[-2])
        beacon_y = self.parse(parts[-1])
        self.loc = Point(x=x, y=y)
        self.closest_beacon = Point(x=beacon_x, y=beacon_y)
        self.manhattan_dist = abs(x - beacon_x) + abs(y - beacon_y)
        self.north = Point(x=x, y=y - self.manhattan_dist)
        self.south = Point(x=x, y=y + self.manhattan_dist)
        self.west = Point(x=x - self.manhattan_dist, y=y)
        self.east = Point(x=x + self.manhattan_dist, y=y)
        self.interval: Optional[Interval] = None

    def reset(self) -> None:
        self.interval = None

    def parse(self, s: str) -> int:
        s = s.rstrip(",:")
        parts = s.split("=")
        return int(parts[-1])

    def get_interval(self) -> Optional[Interval]:
        # case 1
        if self.west.y < self.parent.line_y <= self.south.y:
            up_down = abs(self.parent.line_y - self.loc.y)
            left_right = self.manhattan_dist - up_down
            p1 = Point(x=self.loc.x - left_right, y=self.loc.y + up_down)
            p2 = Point(x=self.loc.x + left_right, y=self.loc.y + up_down)
            return Interval(a=p1, b=p2)
        elif self.west.y >= self.parent.line_y >= self.north.y:  # case 2
            up_down = abs(self.parent.line_y - self.loc.y)
            left_right = self.manhattan_dist - up_down
            p1 = Point(x=self.loc.x - left_right, y=self.loc.y - up_down)
            p2 = Point(x=self.loc.x + left_right, y=self.loc.y - up_down)
            return Interval(a=p1, b=p2)
        else:  # case 3, no intersection
            return None

    def find_interval(self) -> None:
        self.interval = self.get_interval()

    def show(self) -> None:
        text = f"""
Sensor(x={self.loc.x}, y={self.loc.y})
    beacon_x={self.closest_beacon.x}, beacon_y={self.closest_beacon.y}
    north: {self.north}
    east: {self.east}
    south: {self.south}
    west: {self.west}
    interval: {self.interval}
        """.strip()
        print(text)


# ---------------------------------------------------------------------------


class Area:
    def __init__(self, lines: list[str], maxi: int) -> None:
        self.maxi = maxi
        self.sensors: list[Sensor] = []
        self.intervals: list[list[int]] = []
        self.stop = False

        for line in lines:
            self.sensors.append(Sensor(line, self))
        #

    def reset(self):
        self.intervals = []
        for sensor in self.sensors:
            sensor.reset()

    def set_line_y(self, line_y: int) -> None:
        self.line_y = line_y

    def collect_intervals(self) -> None:
        for sensor in self.sensors:
            if sensor.interval:
                a, b = sensor.interval
                x1, x2 = a.x, b.x
                if x1 < 0:
                    x1 = 0
                if x2 > self.maxi:
                    x2 = self.maxi
                self.intervals.append([x1, x2])
            #
        #

    def has_a_hole(self, intervals: list[list[int]]) -> bool:
        total = 0
        for a, b in intervals:
            total += b - a + 1
        #
        return total < self.maxi + 1

    def process_intervals(self) -> None:
        result = helper.merge_intervals(self.intervals)
        if self.has_a_hole(result):
            print("# line:", self.line_y)
            print(result)
            print("---")
            a, b = result[0]
            answer = (b + 1) * 4_000_000 + self.line_y
            print(answer)
            self.stop = True

    def start(self) -> None:
        for sensor in self.sensors:
            sensor.find_interval()
            # sensor.show()
        #
        self.collect_intervals()
        self.process_intervals()

    def show(self) -> None:
        for sensor in self.sensors:
            sensor.show()
        #


# ---------------------------------------------------------------------------


def main():
    # lines = helper.read_lines("example.txt")
    # maxi = 20

    lines = helper.read_lines("input.txt")
    maxi = 4_000_000

    area = Area(lines, maxi)
    # for i in range(3_214_120, maxi + 1):
    for i in range(0, maxi + 1):
        if i % 10_000 == 0:
            print("# i:", i)
        area.reset()
        area.set_line_y(i)
        area.start()
        # ---
        if area.stop:
            break
        #
    #


##############################################################################

if __name__ == "__main__":
    main()
