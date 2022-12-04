from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


class Node:
    def __init__(
        self, name: str, size: int = 0, is_file:
        bool = False,
    ) -> None:
        self.size = size
        self.name = name
        self.childs: list[Node] = []
        self.parent: Node | None = None
        self.is_file = is_file


class Tree:
    def __init__(self) -> None:
        self.root = Node('/')
        self.current_node: Node = self.root

    def add_node(self, node: Node) -> None:
        self.current_node.childs.append(node)
        node.parent = self.current_node
        if node.is_file:
            self.current_node.size += node.size
            # increase size of the all the parents
            parent = self.current_node.parent
            while parent:
                parent.size += node.size
                parent = parent.parent

    def set_current_node(self, name: str) -> None:
        self.current_node = next(
            node for node in self.current_node.childs if node.name == name
        )


def nodes_with_size_lower_than(node: Node, limit: int) -> list[Node]:
    nodes = []
    if not node.is_file and node.size < limit:
        nodes.append(node)
    for child in node.childs:
        _nodes = nodes_with_size_lower_than(child, limit)
        nodes.extend(_nodes)
    return nodes


def compute(s: str) -> int:
    lines = s.splitlines()

    tree = Tree()
    for line in lines:
        if line.startswith('$ cd /'):
            tree.current_node = tree.root
        elif line.startswith('$ cd ..'):
            if tree.current_node.parent:
                tree.current_node = tree.current_node.parent
        elif line.startswith('$ cd '):
            _, _, name = line.split()
            tree.set_current_node(name)
        elif line.startswith('dir'):
            _, name = line.split()
            node = Node(name)
            tree.add_node(node)
        elif line.split()[0].isalnum():
            size, name = line.split()
            node = Node(name, int(size), is_file=True)
            tree.add_node(node)
        # ls
        else:
            pass

    nodes = nodes_with_size_lower_than(tree.root, limit=100000)
    return sum(node.size for node in nodes)


INPUT_S = '''\
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
'''
EXPECTED = 95437


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
