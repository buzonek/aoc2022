from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    matrix = [[int(number) for number in line] for line in s.splitlines()]
    width = len(matrix)
    height = len(matrix[1])

    items: set[tuple[int, int]] = set()

    for row_index in range(1, height-1):
        # go left
        max_l = matrix[row_index][0]
        for column_index in range(1, width-1):
            item = matrix[row_index][column_index]
            if item > max_l:
                max_l = item
                items.add((row_index, column_index))

        max_r = matrix[row_index][-1]
        # go right backwards
        for column_index in range(width - 1, 0, -1):
            item = matrix[row_index][column_index]
            if item > max_r:
                max_r = item
                items.add((row_index, column_index))

    for column_index in range(1, width - 1):
        # go down
        max_u = matrix[0][column_index]
        for row_index in range(1, height - 1):
            item = matrix[row_index][column_index]
            if item > max_u:
                max_u = item
                items.add((row_index, column_index))
        # go up backwards
        max_d = matrix[-1][column_index]
        for row_index in range(height - 1, 0, -1):
            item = matrix[row_index][column_index]
            if item > max_d:
                max_d = item
                items.add((row_index, column_index))

    return len(items) + width*2 + height*2 - 4


INPUT_S = '''\
30373
25512
65332
33549
35390
'''
EXPECTED = 21


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
