from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

ROPE_LEN = 10
ROPE = [[0, 0] for _ in range(ROPE_LEN)]
HEAD = ROPE[0]

visited: set[tuple[int, int]] = {(0, 0)}


def visit(t: list[int, int]) -> None:  # type: ignore
    visited.add(tuple(t))  # type: ignore


def compute(s: str) -> int:
    def fixup() -> None:
        for i in range(ROPE_LEN - 1):
            H, T = ROPE[i], ROPE[i + 1]
            row_distance = H[0] - T[0]
            col_distance = H[1] - T[1]
            if abs(row_distance) < 2 and abs(col_distance) < 2:
                return
            # if they are in the same row
            if H[0] == T[0]:
                ty = (H[1] + T[1]) // 2
                T = [T[0], ty]
            # if they are in the same column
            elif H[1] == T[1]:
                tx = (H[0] + T[0]) // 2
                T = [tx, T[1]]
            # if not in the same row or column
            else:
                if col_distance > 0 and row_distance > 0:
                    T = [T[0] + 1, T[1] + 1]
                elif col_distance > 0 and row_distance < 0:
                    T = [T[0] - 1, T[1] + 1]
                elif col_distance < 0 and row_distance < 0:
                    T = [T[0] - 1, T[1] - 1]
                else:
                    T = [T[0] + 1, T[1] - 1]
            ROPE[i+1] = T
        visit(ROPE[-1])

    for line in s.splitlines():
        direction, steps_s = line.split()
        for _ in range(int(steps_s)):
            if direction == 'D':
                HEAD[0] -= 1
            elif direction == 'U':
                HEAD[0] += 1
            elif direction == 'R':
                HEAD[1] += 1
            else:
                HEAD[1] -= 1
            fixup()
    return len(visited)


INPUT_S = '''\
R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
'''
EXPECTED = 36


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
