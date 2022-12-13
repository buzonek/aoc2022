from __future__ import annotations

import argparse
import dataclasses
import math
import os.path
import typing

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


@dataclasses.dataclass
class Monkey:
    items: list[int]
    operation: typing.Callable[[int], int]
    mod: int
    move_t: int
    move_f: int


def compute(s: str) -> int:
    monkeys = []
    lines = iter(s.splitlines())

    def multiply_by(factor: int) -> typing.Callable[[int], int]:
        def multiply(value: int) -> int:
            return factor * value
        return multiply

    def add(value_to_add: int) -> typing.Callable[[int], int]:
        def _add(value: int) -> int:
            return value_to_add + value
        return _add

    def power() -> typing.Callable[[int], int]:
        def _pow(val: int) -> int:
            return val*val
        return _pow

    while True:
        try:
            next(lines)
            items = list(map(int, next(lines).split('items:')[1].split(', ')))
            oper, val_s = next(lines).split()[-2:]
            if val_s == 'old':
                operation = power()
            else:
                val = int(val_s)
                if oper == '*':
                    operation = multiply_by(val)
                elif oper == '+':
                    operation = add(val)
                else:
                    raise NotImplementedError(oper)
            divade_by = int(next(lines).split()[-1])
            move_to_success = int(next(lines).split()[-1])
            move_to_failure = int(next(lines).split()[-1])
            monkeys.append(
                Monkey(
                    items, operation, divade_by,
                    move_to_success, move_to_failure,
                ),
            )
            next(lines)
        except StopIteration:
            break

    visited = [0] * len(monkeys)
    mod = math.prod(monkey.mod for monkey in monkeys)
    for _ in range(10000):
        for index, monk in enumerate(monkeys):
            for item in monk.items:
                worry_lvl = monk.operation(item) % mod
                idx = monk.move_f if worry_lvl % monk.mod else monk.move_t
                monkeys[idx].items.append(worry_lvl)
                visited[index] += 1
            monk.items.clear()
    visited.sort()
    return visited[-1] * visited[-2]


INPUT_S = '''\
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
'''
EXPECTED = 2713310158


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
