from __future__ import annotations

import argparse
import os.path

import pytest

import support

from collections import Counter

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')



def compute(s: str) -> int:
    numbers = support.parse_numbers_split(s)
    for n in numbers:
        pass

    lines = s.splitlines()
    max = 0
    current_sum = 0
    for line in lines:
        if not line:
            if current_sum > max:
                max = current_sum
            current_sum = 0
        else:
            current_sum += int(line)

    return max


INPUT_S = '''\
120

100
30

300
300

2
'''
EXPECTED = 600


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
