#!/usr/bin/env python3

import pprint
import sys
from dataclasses import dataclass
from typing import NamedTuple

import helper

char = str


@dataclass
class Entry:
    node: char
    dist_from_start: int
    prev_node: char


class Graph:
    def __init__(self, lines: list[str]) -> None:
        self.d: dict[tuple[char, char], int] = self.parse(lines)

    def parse(self, lines: list[str]) -> dict[tuple[char, char], int]:
        d: dict[tuple[char, char], int] = {}

        for line in lines:
            left, right = line.split(":")
            a, b = left.split("-")
            right = int(right)
            d[(a, b)] = right
            d[(b, a)] = right
        #
        return d

    def get_all_nodes(self) -> set[char]:
        result: set[char] = set()

        for a, b in self.d.keys():
            result.add(a)
            result.add(b)
        #
        return result

    def distance_between(self, a: char, b: char) -> int:
        return self.d[(a, b)]

    def __str__(self) -> str:
        return pprint.pformat(self.d)


class Dijkstra:
    def __init__(self, graph: Graph) -> None:
        self.graph = graph
        self.start_node = "a"
        self.visited: set[char] = set()
        self.unvisited: set[char] = self.graph.get_all_nodes()
        self.table: dict[char, Entry] = self.init_table()

    def init_table(self) -> dict[char, Entry]:
        d: dict[char, Entry] = {}
        for c in self.unvisited:
            d[c] = Entry(node=c, dist_from_start=sys.maxsize, prev_node="")
        #
        d[self.start_node].dist_from_start = 0
        #
        return d

    def start(self) -> None:
        while len(self.unvisited) > 0:  # not empty
            entry: Entry = sorted(
                [self.table[k] for k in self.unvisited], key=lambda e: e.dist_from_start
            )[0]
            unvisited_neighbors: set[char] = self.unvisited.difference(entry.node)
            current_value: int = entry.dist_from_start
            for nb in unvisited_neighbors:
                nb_entry: Entry = self.table[nb]
                try:
                    nb_distance: int = self.graph.distance_between(entry.node, nb)
                except KeyError:
                    continue  # the two nodes are not connected
                nb_new_value: int = current_value + nb_distance
                if nb_new_value < nb_entry.dist_from_start:
                    nb_entry.dist_from_start = nb_new_value
                    nb_entry.prev_node = entry.node
                #
            #
            self.unvisited.remove(entry.node)
            self.visited.add(entry.node)

            self.show()
        #

    def show(self) -> None:
        pprint.pprint(self.table)
        print("# visited:", self.visited)
        print("# unvisited:", self.unvisited)
        print("---")
        input("Press ENTER to continue...")


def main():
    lines = helper.read_lines("example.txt")
    # lines = helper.read_lines("input.txt")

    gr = Graph(lines)
    # print(gr)

    dijkstra = Dijkstra(gr)
    dijkstra.start()


##############################################################################

if __name__ == "__main__":
    main()
