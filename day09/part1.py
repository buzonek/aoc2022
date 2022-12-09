from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


visited: set[tuple[int, int]] = set()


def visit(t: list[int, int]) -> None:  # type: ignore
    visited.add(tuple(t))  # type: ignore


def compute(s: str) -> int:
    lines = s.splitlines()
    T,  H = [0, 0], [0, 0]
    visit(T)
    for line in lines:
        direction, steps_s = line.split()
        steps: int = int(steps_s)

        if direction == 'D':
            for _ in range(steps):
                H[0] -= 1
                if H[1] == T[1] and abs(H[0] - T[0]) > 1:
                    T[0] -= 1
                    visit(T)
                    continue
                else:
                    # if distance is to big, catchup
                    if abs(T[0] - H[0]) == 2:
                        T = [H[0] + 1, H[1]]
                        visit(T)
        elif direction == 'U':
            for _ in range(steps):
                H[0] += 1
                if H[1] == T[1] and abs(H[0] - T[0]) > 1:
                    T[0] += 1
                    visit(T)
                    continue
                else:
                    # if distance is to big, catchup
                    if abs(H[0] - T[0]) == 2:
                        T = [H[0] - 1, H[1]]
                        visit(T)
        elif direction == 'R':
            for _ in range(steps):
                H[1] += 1
                if H[0] == T[0] and abs(H[1] - T[1]) > 1:
                    T[1] += 1
                    visit(T)
                    continue
                else:
                    if abs(T[1] - H[1]) == 2:
                        T = [H[0], H[1] - 1]
                        visit(T)
        else:
            for _ in range(steps):
                H[1] -= 1
                if H[0] == T[0] and abs(H[1] - T[1]) > 1:
                    T[1] -= 1
                    visit(T)
                    continue
                else:
                    if abs(T[1] - H[1]) == 2:
                        T = [H[0], H[1] + 1]
                        visit(T)
    return len(visited)


INPUT_S = '''\
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
'''
EXPECTED = 13


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
