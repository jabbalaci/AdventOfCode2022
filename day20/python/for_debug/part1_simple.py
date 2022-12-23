#!/usr/bin/env python3

from typing import Optional

import helper

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
        print("---")


# ---------------------------------------------------------------------------


class Mixer:
    def __init__(self, cl: CircularList) -> None:
        self.cl = cl

    def start(self) -> None:
        for node in self.cl.nodes:
            value = node.value
            print("# moving", value)
            if value == 0:
                continue  # skip 0 value, nothing to do
            elif value > 0:
                for i in range(value):
                    node1 = node
                    node2 = node.next_node
                    self.cl.unlink(node1)
                    self.cl.link(node1, node2)
                #
            else:  # if value < 0
                value = abs(value)
                for i in range(value):
                    node1 = node
                    node2 = node.prev_node.prev_node
                    self.cl.unlink(node1)
                    self.cl.link(node1, node2)
                #
            #
            self.show()
        #

    def get_grove_coordinates(self) -> tuple[int, int, int]:
        li: list[int] = []
        curr = self.cl.get_node_with_value(0)
        for i in range(1000):
            curr = curr.next_node
        #
        li.append(curr.value)
        for i in range(1000):
            curr = curr.next_node
        #
        li.append(curr.value)
        for i in range(1000):
            curr = curr.next_node
        #
        li.append(curr.value)
        #
        return tuple(li)

    def show(self) -> None:
        self.cl.show()


# ---------------------------------------------------------------------------


def main():
    # numbers = helper.read_lines_as_ints("example.txt")
    # numbers = helper.read_lines_as_ints("debug.txt")
    # numbers = helper.read_lines_as_ints("debug2.txt")
    # numbers = helper.read_lines_as_ints("debug3.txt")
    numbers = helper.read_lines_as_ints("debug4.txt")
    # numbers = helper.read_lines_as_ints("input.txt")

    cl = CircularList(numbers)

    mixer = Mixer(cl)
    mixer.show()

    mixer.start()
    a, b, c = mixer.get_grove_coordinates()
    print("#", a, b, c)
    result = sum([a, b, c])
    print(result)


##############################################################################

if __name__ == "__main__":
    main()
