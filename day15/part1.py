from __future__ import annotations

import argparse
import os.path
import re

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

Point = tuple[int, int]

seen: set[Point] = set()
s_to_b: dict[Point, Point] = {}


def manhattan_distance(sensor: Point, beacon: Point) -> int:
    s_x, s_y = sensor
    b_x, b_y = beacon
    return abs(s_x - b_x) + abs(s_y - b_y)


def compute(s: str, row: int = 2000000) -> int:
    lines = s.splitlines()
    for line in lines:
        coordinates_s = re.findall(r'x=(-?\d+), y=(-?\d+)', line)
        coordinates = [(int(x), int(y)) for x, y in coordinates_s]
        s_to_b[coordinates[0]] = coordinates[1]

    for sensor in s_to_b.keys():
        sx, sy = sensor
        dist = manhattan_distance(sensor, s_to_b[sensor])
        if sy >= row and sy - dist <= row:
            for delta in range(dist + 1):
                remaining = dist - delta
                if sy - remaining <= row:
                    seen.add((sx - delta, row))
                    seen.add((sx + delta, row))
                else:
                    break
        if sy <= row and sy + dist >= row:
            for delta in range(dist + 1):
                remaining = dist - delta
                if sy + remaining >= row:
                    seen.add((sx + delta, row))
                    seen.add((sx - delta, row))
                else:
                    break
    beacons = [b for b in set(s_to_b.values()) if b[1] == row]
    return len(seen) - len(beacons)


INPUT_S = '''\
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
'''
EXPECTED = 26


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s, 10) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
