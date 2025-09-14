from collections import Counter
from math import log10

import sys


def parse(lines):
    line = next(lines).strip()
    return ((int(part) for part in line.split(" ")),)


def iterate(stone):
    if stone == 0:
        yield 1
    elif (p := int(log10(stone))) % 2 == 0:
        yield stone * 2024
    else:
        m = 10 ** ((p + 1) // 2)
        yield stone // m
        yield stone % m


def iterate_all(stones):
    for stone in stones:
        yield from iterate(stone)


def part1(stones):
    for _ in range(25):
        stones = iterate_all(stones)
    return sum(1 for _ in stones)


def part2(stones):
    stones = Counter(stones)
    for _ in range(75):
        next_stones = Counter()
        for stone, count in stones.items():
            for ns in iterate(stone):
                next_stones[ns] += count
        stones = next_stones
    return stones.total()


if __name__ == "__main__":
    print(part2(*parse(sys.stdin)))
