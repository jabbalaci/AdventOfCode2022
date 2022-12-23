#!/usr/bin/env python3

from typing import Optional

import helper

# DEBUG = True
DEBUG = False

# ---------------------------------------------------------------------------


class Node:
    def __init__(self, data: int) -> None:
        self.value: int = data
        self.prev_node: Optional[Node] = None
        self.next_node: Optional[Node] = None


# ---------------------------------------------------------------------------


class CircularList:
    def __init__(self, numbers: list[int]) -> None:
        self.nodes = [Node(n) for n in numbers]
        for i in range(len(self.nodes)):
            prev = self.nodes[i - 1]
            curr = self.nodes[i]
            prev.next_node = curr
            curr.prev_node = prev
        #
        self.head = self.nodes[0]

    def get_node_with_value(self, value: int) -> Optional[Node]:
        for node in self.nodes:
            if node.value == value:
                return node
            #
        #
        return None

    def unlink(self, node: Node) -> Node:
        node.prev_node.next_node = node.next_node
        node.next_node.prev_node = node.prev_node
        return node

    def link(self, node1: Node, node2: Node) -> Node:
        """
        link node1 after node2
        """
        node3 = node2.next_node
        node2.next_node = node1
        node1.prev_node = node2
        node1.next_node = node3
        node3.prev_node = node1
        return node1

    def show(self) -> None:
        curr = self.nodes[0]
        for _ in range(len(self.nodes)):
            print(curr.value, end=", ")
            curr = curr.next_node
        #
        print()


# ---------------------------------------------------------------------------


class Mixer:
    def __init__(self, cl: CircularList) -> None:
        self.cl = cl

    def start(self) -> None:
        for node in self.cl.nodes:
            value = node.value
            if value == 0:
                continue  # skip 0 value, nothing to do
            #
            if DEBUG:
                print("# moving", value)
            node1 = node  # to be unlinked
            node2 = node
            move = value % len(self.cl.nodes)

            # special case
            if move == 0:  # and value != 0
                if value > 0:
                    node2 = node1.next_node
                else:
                    node2 = node1.prev_node.prev_node
                #
                self.cl.unlink(node1)
                self.cl.link(node1, node2)
                continue
            #

            # else, non-special case
            if value < 0:
                move -= 1
            #
            if move == 0:  # yet another special case, the element won't move
                continue
            #
            for _ in range(move):
                node2 = node2.next_node
            #

            # unlink node1
            self.cl.unlink(node1)
            # link node1 after node2
            self.cl.link(node1, node2)
            #
            if DEBUG:
                self.show()
        #

    def get_grove_coordinates(self) -> tuple[int, int, int]:
        li: list[int] = []
        curr = self.cl.get_node_with_value(0)
        for i in range(3):
            move = 1000 % len(self.cl.nodes)
            for _ in range(move):
                curr = curr.next_node
            #
            li.append(curr.value)
        #
        return tuple(li)

    def show(self) -> None:
        self.cl.show()


# ---------------------------------------------------------------------------


def main():
    # numbers = helper.read_lines_as_ints("debug.txt")
    # numbers = helper.read_lines_as_ints("debug2.txt")
    # numbers = helper.read_lines_as_ints("debug3.txt")
    numbers = helper.read_lines_as_ints("example.txt")
    # numbers = helper.read_lines_as_ints("input.txt")

    cl = CircularList(numbers)

    mixer = Mixer(cl)
    if DEBUG:
        mixer.show()

    mixer.start()
    a, b, c = mixer.get_grove_coordinates()
    print("#", a, b, c)
    result = sum([a, b, c])
    print(result)


##############################################################################

if __name__ == "__main__":
    main()
