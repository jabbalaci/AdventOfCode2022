#!/usr/bin/env python3

import sys

import helper


class Screen:
    def __init__(self) -> None:
        self.pixels: list[int] = [0] * (40 * 6)

    def update(self, cycles: int, cpu_x: int) -> None:
        diff = abs((cycles % 40) - cpu_x)  # modulo trick
        if diff <= 1:
            self.pixels[cycles] = 1

    def show(self) -> None:
        for i in range(len(self.pixels)):
            value = self.pixels[i]
            c = "."
            if value == 1:
                c = "#"
            if i > 0 and i % 40 == 0:
                print()
            sys.stdout.write(c)
        #


class Computer:
    def __init__(self) -> None:
        self.screen = Screen()
        self.cycles = 0
        self.cpu_x = 1

    def inc_cycles(self) -> None:
        self.screen.update(self.cycles, self.cpu_x)
        self.cycles += 1

    def execute(self, line) -> None:
        parts = line.split()
        if parts[0] == "noop":
            self.inc_cycles()
        else:  # addx
            value = int(parts[1])
            self.inc_cycles()
            self.inc_cycles()
            self.cpu_x += value


def main():
    # lines = helper.read_lines("example2.txt")
    lines = helper.read_lines("input.txt")

    computer = Computer()

    for line in lines:
        computer.execute(line)
    #

    computer.screen.show()


##############################################################################

if __name__ == "__main__":
    main()
