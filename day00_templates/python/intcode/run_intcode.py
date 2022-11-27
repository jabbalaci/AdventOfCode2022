#!/usr/bin/env python3

from enum import Enum
from typing import Dict, List, NamedTuple, Tuple

import helper


class ShouldNeverGetHere(Exception):
    pass


class Mode(Enum):
    POSITION_MODE = 0
    IMMEDIATE_MODE = 1
    RELATIVE_MODE = 2


class Instruction(NamedTuple):
    opcode: int
    first_param_mode: Mode
    second_param_mode: Mode
    third_param_mode: Mode


def read_instruction(number: int) -> Instruction:
    # print("# number:", number)
    #
    def to_mode(c: str) -> Mode:
        if c == '0':
            return Mode.POSITION_MODE
        if c == '1':
            return Mode.IMMEDIATE_MODE
        if c == '2':
            return Mode.RELATIVE_MODE
        raise ShouldNeverGetHere()

    if number == 99:
        # special case, it'll halt the program; parameter modes are not used, they get a dummy value
        return Instruction(opcode=number, first_param_mode=Mode.POSITION_MODE,
                           second_param_mode=Mode.POSITION_MODE, third_param_mode=Mode.POSITION_MODE)

    s = str(number)
    if len(s) == 1:
        opcode = number
        first_param_mode = second_param_mode = third_param_mode = Mode.POSITION_MODE    # default
    else:
        opcode = int(s[-2:].replace("0", ""))
        params = s[:-2].zfill(3)
        first_param_mode = to_mode(params[-1])
        second_param_mode = to_mode(params[-2])
        third_param_mode = to_mode(params[-3])
    #
    return Instruction(opcode=opcode, first_param_mode=first_param_mode,
                       second_param_mode=second_param_mode, third_param_mode=third_param_mode)


###############
## Amplifier ##
###############

class Amplifier:
    def __init__(self, program: Tuple[int, ...]) -> None:
        self.program = program                  # immutable backup
        self.reset()

    def reset(self):
        self.data = list(self.program)          # mutable copy
        self.idx = 0                            # instruction pointer
        self.prg_input: List[int] = []          # will be set later
        self.prg_output = 0                     # will be set later
        self.relative_base = 0                  # default value of it
        self.extra_mem: Dict[int, int] = {}     # extra memory is represented as a dictionary

    def set_input(self, data: List[int]) -> None:
        self.prg_input = data[:]

    def read_input(self) -> int:
        # return self.prg_input
        #res = input("Input: ")
        return self.prg_input.pop(0)

    def get_output(self) -> int:
        return self.prg_output

    def read(self, idx: int) -> int:
        """
        Read the value of a cell. If it's outside of the
        program, then read from the extra memory.
        """
        try:
            return self.data[idx]
        except IndexError:
            try:
                return self.extra_mem[idx]
            except KeyError:
                self.extra_mem[idx] = 0
                return 0

    def save(self, idx: int, value: int) -> None:
        """
        Save a value to a given index position. If it falls
        outside of the program, store it in the extra memory.
        """
        try:
            self.data[idx] = value
        except IndexError:
            self.extra_mem[idx] = value

    def debug(self) -> None:
        print(self.extra_mem)

    def run(self) -> None:
        #
        def get_param(data: List[int], value: int, mode: Mode) -> int:
            if mode == Mode.IMMEDIATE_MODE:
                result = value
            elif mode == Mode.POSITION_MODE:
                pos = value
                result = self.read(idx=pos)
            elif mode == Mode.RELATIVE_MODE:
                pos = self.relative_base + value
                result = self.read(idx=pos)
            else:
                raise ShouldNeverGetHere()
            #
            return result
        # enddef get_param

        def where_to(data: List[int], value: int, mode: Mode) -> int:
            if mode == Mode.POSITION_MODE:
                result = value
            elif mode == Mode.RELATIVE_MODE:
                result = self.relative_base + value
            else:
                raise ShouldNeverGetHere()
            #
            return result
        # enddef where_to

        inst: Instruction = read_instruction(self.data[self.idx])
        while inst.opcode != 99:
            if inst.opcode == 1:    # add
                inp1 = get_param(self.data, self.data[self.idx + 1], inst.first_param_mode)
                inp2 = get_param(self.data, self.data[self.idx + 2], inst.second_param_mode)
                pos = where_to(self.data, self.data[self.idx + 3], inst.third_param_mode)
                self.save(idx=pos, value=(inp1 + inp2))
                self.idx += 4
            elif inst.opcode == 2:    # multiply
                inp1 = get_param(self.data, self.data[self.idx + 1], inst.first_param_mode)
                inp2 = get_param(self.data, self.data[self.idx + 2], inst.second_param_mode)
                pos = where_to(self.data, self.data[self.idx + 3], inst.third_param_mode)
                self.save(idx=pos, value=(inp1 * inp2))
                self.idx += 4
            elif inst.opcode == 3:    # input
                inp = self.read_input()
                pos = where_to(self.data, self.data[self.idx + 1], inst.first_param_mode)
                self.save(idx=pos, value=inp)
                self.idx += 2
            elif inst.opcode == 4:    # output
                value = get_param(self.data, self.data[self.idx + 1], inst.first_param_mode)
                self.prg_output = value      # save last output
                # print("Output:", value)      # print output
                # print(value, end="")
                self.idx += 2
            elif inst.opcode == 5:    # jump-if-true
                inp1 = get_param(self.data, self.data[self.idx + 1], inst.first_param_mode)
                inp2 = get_param(self.data, self.data[self.idx + 2], inst.second_param_mode)
                if inp1 != 0:
                    self.idx = inp2
                else:
                    self.idx += 3
            elif inst.opcode == 6:    # jump-if-false
                inp1 = get_param(self.data, self.data[self.idx + 1], inst.first_param_mode)
                inp2 = get_param(self.data, self.data[self.idx + 2], inst.second_param_mode)
                if inp1 == 0:
                    self.idx = inp2
                else:
                    self.idx += 3
            elif inst.opcode == 7:    # less than
                inp1 = get_param(self.data, self.data[self.idx + 1], inst.first_param_mode)
                inp2 = get_param(self.data, self.data[self.idx + 2], inst.second_param_mode)
                pos = where_to(self.data, self.data[self.idx + 3], inst.third_param_mode)
                if inp1 < inp2:
                    self.save(idx=pos, value=1)
                else:
                    self.save(idx=pos, value=0)
                #
                self.idx += 4
            elif inst.opcode == 8:    # equals
                inp1 = get_param(self.data, self.data[self.idx + 1], inst.first_param_mode)
                inp2 = get_param(self.data, self.data[self.idx + 2], inst.second_param_mode)
                pos = where_to(self.data, self.data[self.idx + 3], inst.third_param_mode)
                if inp1 == inp2:
                    self.save(idx=pos, value=1)
                else:
                    self.save(idx=pos, value=0)
                #
                self.idx += 4
            elif inst.opcode == 9:    # relative base offset
                value = get_param(self.data, self.data[self.idx + 1], inst.first_param_mode)
                self.relative_base += value
                self.idx += 2
            else:
                raise ShouldNeverGetHere()    # invalid opcode

            if self.idx < 0:
                raise ShouldNeverGetHere()
            # endif
            inst = read_instruction(self.data[self.idx])
            # input("Press ENTER to continue...")
            # self.debug()
        # endwhile
    # enddef run
# endclass


def main() -> None:
    line = helper.read_lines("input.txt")[0]
    program = tuple([int(n) for n in line.split(",")])
    ampl = Amplifier(program)
    size = 50
    for y in range(size):
        for x in range(size):
            ampl.reset()
            ampl.set_input([x, y])
            ampl.run()
            out = ampl.get_output()
            print(out, end="")
        #
        print()
    #

##############################################################################

if __name__ == "__main__":
    main()
