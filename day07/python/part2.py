#!/usr/bin/env python3

from enum import Enum, auto
from pprint import pprint

import helper


class FileSystem:
    pwd: list[str] = []

    @classmethod
    def get_cwd(cls):
        return "/".join(cls.pwd).replace("//", "/")

    @classmethod
    def enter(cls, dname):
        cls.pwd.append(dname)

    @classmethod
    def go_up(cls):
        cls.pwd.pop()


class FileType(Enum):
    DIR = auto()
    FILE = auto()


class Entry:
    def __init__(self, name: str, type: FileType, size: int = 0):
        cwd = FileSystem.get_cwd()
        if cwd.endswith("/"):
            self.name = cwd + name
        else:
            self.name = "/".join([cwd, name])  # .replace("//", "/")
        self.type = type
        self.size = size

    def get_size(self, tree: "Tree") -> int:
        if self.type == FileType.FILE:
            return self.size
        else:
            return get_dir_size(tree, tree.d[self.name])

    def __str__(self) -> str:
        return f"{self.name} ({self.type.name}, {self.size})"

    def __repr__(self):
        return str(self)


class Tree:
    def __init__(self):
        self.d: dict[str, list[Entry]] = {}

    def add(self, entry: Entry) -> None:
        key = FileSystem.get_cwd()
        if key in self.d:
            self.d[key].append(entry)
        else:
            self.d[key] = [entry]
        #

    def show(self) -> None:
        pprint(self.d)


def process_entry(tree: Tree, entry: str) -> None:
    parts = entry.split()
    if parts[0] == "dir":
        name = parts[1]
        tree.add(Entry(name, FileType.DIR))
    else:
        size = int(parts[0])
        name = parts[1]
        tree.add(Entry(name, FileType.FILE, size))


def process_command(cmd: str) -> None:
    cmd = cmd.removeprefix("$ ")
    parts = cmd.split()
    if parts[0] == "cd":
        dest = parts[1]
        if dest == "..":
            FileSystem.go_up()
        else:
            FileSystem.enter(dest)
        #
    #


def get_dir_size(tree: Tree, entries: list[Entry]) -> int:
    total = 0
    for e in entries:
        total += e.get_size(tree)
    #
    return total


def calculate_dir_sizes(tree: Tree) -> dict[str, int]:
    result: dict[str, int] = {}
    for dname, entries in tree.d.items():
        # print("{0}: {1} bytes".format(dname, get_dir_size(tree, entries)))
        result[dname] = get_dir_size(tree, entries)
    #
    return result


def main():
    # lines = helper.read_lines("example.txt")
    lines = helper.read_lines("input.txt")

    tree = Tree()
    for line in lines:
        if line.startswith("$ "):
            process_command(line)
        else:
            process_entry(tree, line)
        #
    #
    tree.show()
    print("---")
    result = calculate_dir_sizes(tree)
    pprint(result)
    print("---")
    limit = 30_000_000 - (70_000_000 - result["/"])
    candidates = []
    for _, v in result.items():
        if v >= limit:
            candidates.append(v)
        #
    #
    answer = min(candidates)
    print(answer)


##############################################################################

if __name__ == "__main__":
    main()
