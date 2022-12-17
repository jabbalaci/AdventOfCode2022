#!/usr/bin/env python3

from typing import Optional

import helper
from helper import Interval, Point


class Sensor:
    def __init__(self, line: str, parent: "Area") -> None:
        self.line_y = parent.line_y
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

    def parse(self, s: str) -> int:
        s = s.rstrip(",:")
        parts = s.split("=")
        return int(parts[-1])

    def get_interval(self) -> Optional[Interval]:
        # case 1
        if self.west.y < self.line_y <= self.south.y:
            up_down = abs(self.line_y - self.loc.y)
            left_right = self.manhattan_dist - up_down
            p1 = Point(x=self.loc.x - left_right, y=self.loc.y + up_down)
            p2 = Point(x=self.loc.x + left_right, y=self.loc.y + up_down)
            return Interval(a=p1, b=p2)
        elif self.west.y >= self.line_y >= self.north.y:  # case 2
            up_down = abs(self.line_y - self.loc.y)
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
    def __init__(self, lines: list[str], line_y: int) -> None:
        self.line_y = line_y
        self.sensors: list[Sensor] = []
        self.intervals: list[tuple[int, int]] = []

        for line in lines:
            self.sensors.append(Sensor(line, self))
        #

    def collect_intervals(self) -> None:
        for sensor in self.sensors:
            if sensor.interval:
                a, b = sensor.interval
                x1, x2 = a.x, b.x
                self.intervals.append((x1, x2))
            #
        #

    def process_intervals(self) -> None:
        result = set()
        for a, b in self.intervals:
            # print(f"[{a}, {b}]")
            for e in range(a, b + 1):
                result.add(e)
            #
        #
        for sensor in self.sensors:
            if sensor.closest_beacon.y == self.line_y:
                try:
                    result.remove(sensor.closest_beacon.x)
                except:
                    pass
            #
        #
        # print(result)
        # print("---")
        print(len(result))

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
    # line_y = 10

    lines = helper.read_lines("input.txt")
    line_y = 2_000_000

    area = Area(lines, line_y)
    area.start()


##############################################################################

if __name__ == "__main__":
    main()
