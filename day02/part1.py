from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    rules = {
        'A': {
            'X': 4,
            'Y': 8,
            'Z': 3,
        },
        'B': {
            'X': 1,
            'Y': 5,
            'Z': 9,
        },
        'C': {
            'X': 7,
            'Y': 2,
            'Z': 6,
        },
    }
    lines = s.splitlines()
    points = 0
    for line in lines:
        player1_choice, player2_choice = line.split(' ')
        points += rules[player1_choice][player2_choice]
    return points


INPUT_S = '''\
C Z
B X
A X
'''
EXPECTED = 11


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
