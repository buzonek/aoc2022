from __future__ import annotations

import argparse
import os.path

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

WIDTH = 40
HEIGHT = 6


def compute(s: str) -> None:
    cycle_count = 0
    register = 1
    matrix = [['_' for _ in range(WIDTH)] for _ in range(HEIGHT)]

    def draw_pixel() -> None:
        nonlocal cycle_count
        pixel_pos = cycle_count % 40
        row = cycle_count // 40
        matrix[row][pixel_pos] = '#' if pixel_pos in range(
            register-1, register + 2,
        ) else '.'
        cycle_count += 1
        return

    lines = s.splitlines()
    for line in lines:
        if line.startswith('noop'):
            draw_pixel()
        else:
            _, v = line.split()
            draw_pixel()
            draw_pixel()
            register += int(v)
    print('\n'.join(' '.join(char for char in row) for row in matrix))
    return None


INPUT_S = '''\
addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop
'''
EXPECTED = '##..##..'


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        compute(f.read())
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
