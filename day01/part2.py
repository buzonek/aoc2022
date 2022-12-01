from __future__ import annotations

import argparse
import os.path

import bisect
import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')



def compute(s: str) -> int:
    chunks = s.split('\n\n')
    items = []
    for chunk in chunks:
        s = sum(int(x) for x in chunk.split())
        items.append(s)
    items.sort()
    return sum(items[-3:])


INPUT_S = '''\
99

102

50
50

122

100
30

300
300

2

12
32

1

34
54
'''
EXPECTED = 852


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
