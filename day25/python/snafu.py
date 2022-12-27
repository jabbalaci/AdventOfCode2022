#!/usr/bin/env python3

char = str


def snafu2decimal(snafu: str) -> int:
    result = 0

    for idx, c in enumerate(snafu[::-1]):
        if c == "-":
            value = -1
        elif c == "=":
            value = -2
        else:
            value = int(c)
        #
        result += value * (5**idx)
    #

    return result


def to_value(c: char, base: int, power: int) -> int:
    if c == "-":
        value = -1
    elif c == "=":
        value = -2
    else:
        value = int(c)
    #
    return value * base**power


def decimal2snafu(decimal: int) -> str:
    number = decimal
    i = 0
    li = []
    while True:
        value1 = 1 * 5**i
        value2 = 2 * 5**i
        diff1 = abs(decimal - value1)
        diff2 = abs(decimal - value2)
        if value1 >= decimal or value2 >= decimal:
            mini = min([diff1, diff2])
            d = {diff1: "1", diff2: "2"}
            li.append(d[mini])
            number += -1 * to_value(d[mini], 5, i)
            break
        # else
        li.append("0")
        i += 1
    #
    i = len(li) - 2
    while i >= 0:
        value0 = 0
        value1 = 1 * 5**i
        value2 = 2 * 5**i
        value_m1 = -1 * 5**i
        value_m2 = -2 * 5**i
        diff0 = abs(number - value0)
        diff1 = abs(number - value1)
        diff2 = abs(number - value2)
        diff_m1 = abs(number - value_m1)
        diff_m2 = abs(number - value_m2)
        mini = min([diff0, diff1, diff2, diff_m1, diff_m2])
        d = {diff0: "0", diff1: "1", diff2: "2", diff_m1: "-", diff_m2: "="}
        li[i] = d[mini]
        number += -1 * to_value(d[mini], 5, i)
        i -= 1
    #
    return "".join(li[::-1])


##############################################################################


def test_decimal2snafu(d: dict[int, str]) -> None:
    for dec, snafu in d.items():
        result = decimal2snafu(dec)
        print(f"{dec}: {result}")
    #


def run_tests1(d: dict[int, str]) -> None:
    print("Running tests #1")
    for dec, snafu in d.items():
        assert snafu2decimal(snafu) == dec
    #


def run_tests2(d: dict[int, str]) -> None:
    print("Running tests #2")
    for dec, snafu in d.items():
        assert decimal2snafu(dec) == snafu
    #


##############################################################################

if __name__ == "__main__":
    # Decimal          SNAFU
    examples = """
        1              1
        2              2
        3             1=
        4             1-
        5             10
        6             11
        7             12
        8             2=
        9             2-
       10             20
       15            1=0
       20            1-0
     2022         1=11-2
    12345        1-0---0
314159265  1121-1110-1=0
""".strip()
    d = {int(line.split()[0]): line.split()[1] for line in examples.splitlines()}

    run_tests1(d)
    run_tests2(d)
    print("done")
