from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    lines = s.splitlines()
    matrix: list[list[int]] = [[] for _ in range(len(lines))]
    for index, line in enumerate(lines):
        matrix[index] = [int(number) for number in line]
    width = len(matrix)
    height = len(matrix[1])
    cnt = 0
    for row_index in range(1, width-1):
        for column_index in range(1, height-1):
            item = matrix[row_index][column_index]
            # verify left
            if all(num < item for num in matrix[row_index][:column_index]):
                cnt += 1
                continue
            # right
            if all(num < item for num in matrix[row_index][column_index + 1:]):
                cnt += 1
                continue
            # up
            if all(row[column_index] < item for row in matrix[:row_index]):
                cnt += 1
                continue
            # down
            if all(row[column_index] < item for row in matrix[row_index + 1:]):
                cnt += 1
                continue
    # add all on the edge
    cnt += width*2 + height*2 - 4

    return cnt


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
