import sys
import re
from collections import defaultdict
from math import copysign
from functools import reduce
from operator import mul


def parse(lines):
    line_regex = re.compile(r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)")
    m, n = [int(w) for w in next(lines).strip().split(" ")]
    groups = []
    return (
        m,
        n,
        [
            [int(w) for w in line_regex.match(line.strip()).groups()]
            for line in lines
        ],
    )


def part1(m, n, groups):
    quadrants = defaultdict(int)
    for x, y, vx, vy in groups:
        fx = (x + vx * 100) % m - (m - 1) // 2
        fy = (y + vy * 100) % n - (n - 1) // 2
        if fx and fy:
            quadrants[(copysign(1, fx), copysign(1, fy))] += 1
    print(quadrants)
    return reduce(mul, quadrants.values(), 1)


def part2(m, n, groups): ...


if __name__ == "__main__":
    print(part2(*parse(sys.stdin)))
