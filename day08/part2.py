from __future__ import annotations

import argparse
import os.path
import typing

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def count_while(max: int, items: typing.Iterable[int]) -> int:
    cnt = 0
    for item in items:
        if item < max:
            cnt += 1
        else:
            cnt += 1
            break
    return cnt


def compute(s: str) -> int:
    lines = s.splitlines()
    matrix: list[list[int]] = [[] for _ in range(len(lines))]
    for index, line in enumerate(lines):
        matrix[index] = [int(number) for number in line]
    width = len(matrix)
    height = len(matrix[1])
    scores = [[0 for _ in range(width)] for _ in range(height)]
    for row_index in range(1, width-1):
        for column_index in range(1, height-1):
            item = matrix[row_index][column_index]
            lf = count_while(item, reversed(matrix[row_index][:column_index]))
            rg = count_while(item, matrix[row_index][column_index + 1:])
            up = count_while(
                item, reversed(
                    [row[column_index] for row in matrix[:row_index]],
                ),
            )
            dw = count_while(
                item, (
                    row[column_index]
                    for row in matrix[row_index + 1:]
                ),
            )
            scores[row_index][column_index] = lf * rg * up * dw
    row_max = [max(row) for row in scores]
    return max(row_max)


INPUT_S = '''\
30373
25512
65332
33549
35390
'''
EXPECTED = 8


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
