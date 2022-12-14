from __future__ import annotations

import argparse
import heapq
import os.path
from typing import Generator

import pytest

import support
INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

Point = tuple[int, int]


def get_neighbours(point: Point, size: Point) -> Generator[Point, None, None]:
    x, y = point
    if x - 1 >= 0:
        yield (x - 1, y)
    if x + 1 <= size[0]:
        yield (x + 1, y)
    if y - 1 >= 0:
        yield (x, y - 1)
    if y + 1 <= size[1]:
        yield (x, y + 1)


def dijkstra(graph: dict[Point, int], start: Point, end: Point) -> int:
    graph_size = (max(graph)[0], max(graph, key=lambda x: x[1])[1])
    heap: list[tuple[int, Point]] = []
    distances: dict[Point, int] = {}
    distances[start] = 0
    heapq.heappush(heap, (0, start))

    while heap:
        dist, node = heapq.heappop(heap)
        node_val = graph[node]
        if node == end:
            return distances[node]

        for neighbor in get_neighbours(node, graph_size):
            new_dist = dist + 1
            neighbor_val = graph[(neighbor)]
            if node_val - neighbor_val >= -1:
                if neighbor not in distances or new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    heapq.heappush(heap, (new_dist, neighbor))
    return 10000000


mapping = {
    'S': 'a',
    'E': 'z',
}


def compute(s: str) -> int:
    graph = {}
    start, stop = (0, 0), (0, 0)
    for x, row in enumerate(s.splitlines()):
        for y, c in enumerate(row):
            if c == 'S':
                start = (x, y)
            elif c == 'E':
                stop = (x, y)
            graph[(x, y)] = ord(mapping.get(c, c))
    return dijkstra(graph, start, stop)


INPUT_S = '''\
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
'''
EXPECTED = 31


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
