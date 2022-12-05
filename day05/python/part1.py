#!/usr/bin/env python3

import helper


def process_header(text: str) -> dict[int, list[str]]:
    d: dict[int, list[str]] = {}

    lines = text.splitlines()[::-1]
    # for line in lines:
    # print(line)
    #
    # print("---")
    numbers = [int(digit) for digit in lines[0].split()]
    length = len(lines[1])
    for n in numbers:
        d[n] = []
    #
    for line in lines[1:]:
        if len(line) < length:
            line = line + " " * (length - len(line))
        # print("'" + line + "'")
        chars = line[1::4]
        # print("'" + chars + "'")
        for idx, c in enumerate(chars, start=1):
            if c != " ":
                d[idx].append(c)
            #
        #
    #
    return d


def process_body(d: dict[int, list[str]], body: str) -> dict[int, list[str]]:
    lines = body.splitlines()
    for line in lines:
        parts = line.split()
        how_many = int(parts[1])
        from_stack = int(parts[3])
        to_stack = int(parts[-1])
        # print(line)
        # print(how_many, from_stack, to_stack)
        for i in range(how_many):
            elem = d[from_stack].pop()
            d[to_stack].append(elem)
        #
    #
    return d


def show(d: dict[int, list[str]]) -> None:
    for k, v in d.items():
        print(k, v)
    print("---")


def main():
    # content = helper.read("example.txt")
    content = helper.read("input.txt")

    header, body = content.split("\n\n")

    d = process_header(header)
    # show(d)
    d = process_body(d, body)
    # show(d)

    result = ""
    for k in sorted(d):
        result += d[k][-1]
    #
    print(result)


##############################################################################

if __name__ == "__main__":
    main()
