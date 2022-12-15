from __future__ import annotations

import argparse
import itertools
import os.path
from functools import cmp_to_key

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

ListInput = int | list['ListInput']


def compute(s: str) -> int:
    def compare(first: ListInput, second: ListInput) -> int:
        if isinstance(first, int) and isinstance(second, int):
            if first < second:
                return 1
            elif first == second:
                return 0
            else:
                return -1
        elif isinstance(first, list) and isinstance(second, list):
            for first, second in itertools.zip_longest(first, second):
                if first is None:
                    return 1
                if second is None:
                    return -1
                compared = compare(first, second)
                if compared == 0:
                    continue
                else:
                    return compared
            return 0
        elif isinstance(first, int):
            return compare([first], second)
        else:
            return compare(first, [second])

    items = [eval(line) for line in s.splitlines() if line]
    items.append([[6]])
    items.append([[2]])
    items.sort(key=cmp_to_key(compare), reverse=True)
    return (items.index([[6]]) + 1) * (items.index([[2]]) + 1)


INPUT_S = '''\
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
'''
EXPECTED = 140


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
