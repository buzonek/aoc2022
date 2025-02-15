from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    rules = {
        'A': {
            'X': 3,
            'Y': 4,
            'Z': 8,
        },
        'B': {
            'X': 1,
            'Y': 5,
            'Z': 9,
        },
        'C': {
            'X': 2,
            'Y': 6,
            'Z': 7,
        },
    }
    lines = s.splitlines()
    points = 0
    for line in lines:
        player1_choice, end_result = line.split(' ')
        points += rules[player1_choice][end_result]
    return points


INPUT_S = '''\
A X
C Z
B Z
'''
EXPECTED = 19


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
