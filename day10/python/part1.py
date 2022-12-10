#!/usr/bin/env python3

import helper


class CPU:
    milestones = (20, 60, 100, 140, 180, 220)

    def __init__(self) -> None:
        self.cycles = 0
        self.x = 1
        self.result = 0

    def inc_cycles(self) -> None:
        self.cycles += 1
        if self.cycles in CPU.milestones:
            # print(f"{self.cycles}: {self.x}")
            self.result += self.cycles * self.x

    def execute(self, line) -> None:
        parts = line.split()
        if parts[0] == "noop":
            self.inc_cycles()
        else:  # addx
            value = int(parts[1])
            self.inc_cycles()
            self.inc_cycles()
            self.x += value


def main():
    # lines = helper.read_lines("example1.txt")
    # lines = helper.read_lines("example2.txt")
    lines = helper.read_lines("input.txt")

    cpu = CPU()

    for line in lines:
        cpu.execute(line)
    #
    # print(cpu.x)
    # print("---")
    print(cpu.result)


##############################################################################

if __name__ == "__main__":
    main()
