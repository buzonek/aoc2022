from __future__ import annotations

import argparse
import os.path
import re

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> str:
    head, tail = s.split('\n\n')

    head_lines = head.splitlines()
    crates_no = int(head_lines.pop().split().pop())
    crates: list[list[str]] = [[] for _ in range(crates_no)]

    for line in head_lines:
        crate_idx = 0
        chars = iter(line)
        while True:
            try:
                chunk = next(chars) + next(chars) + next(chars)
                # if these 3 characters represents [*letter*]
                if chunk.strip():
                    crates[crate_idx].insert(0, chunk[1])
                next(chars)
                crate_idx += 1
            except StopIteration:
                break

    for line in tail.splitlines():
        matches = re.search(r'move (\d+) from (\d+) to (\d+)', line)
        if not matches:
            return ''
        move_cnt, _from, _to = map(int, matches.groups())
        for _ in range(move_cnt):
            crates[_to - 1].append(crates[_from - 1].pop())
    return ''.join(crate[-1] for crate in crates)


INPUT_S = '''\
    [D]
[N] [C]
[Z] [M] [P]
 1   2   3

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
'''
EXPECTED = 'CMZ'


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
