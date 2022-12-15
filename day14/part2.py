from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    coords = set()
    lines = s.splitlines()
    for line in lines:
        parts = line.split(' -> ')
        for start, end in zip(parts[:-1], parts[1:]):
            startx, starty = map(int, start.split(','))
            endx, endy = map(int, end.split(','))

            s_x, e_x = min(startx, endx), max(startx, endx)
            s_y, e_y = min(starty, endy), max(starty, endy)
            for x in range(s_x, e_x + 1):
                for y in range(s_y, e_y + 1):
                    coords.add((x, y))

    max_y = max(coords, key=lambda c: c[1])[1] + 2
    for x in range(500 - max_y - 1, 500 + max_y + 1):
        coords.add((x, max_y))

    sands_dropped = 0
    while True:
        sand_pos = (500, 0)
        while True:
            next_pos = (sand_pos[0], sand_pos[1] + 1)
            if next_pos not in coords:
                sand_pos = next_pos
            # cant move there
            else:
                # try move diagonally left
                next_pos = (sand_pos[0] - 1, sand_pos[1] + 1)
                if next_pos not in coords:
                    sand_pos = next_pos
                else:
                    # try diagonally right
                    next_pos = (sand_pos[0] + 1, sand_pos[1] + 1)
                    if next_pos not in coords:
                        sand_pos = next_pos
                    else:
                        # cant move left or right
                        coords.add(sand_pos)
                        sands_dropped += 1
                        if sand_pos == (500, 0):
                            return sands_dropped
                        break


INPUT_S = '''\
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
'''
EXPECTED = 93


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
