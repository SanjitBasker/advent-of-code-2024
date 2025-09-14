import sys
from collections import defaultdict
from itertools import combinations
from math import gcd


def parse(lines):
    grid = [list(line.strip()) for line in lines]
    antennae_groups = defaultdict(list)
    for i, row in enumerate(grid):
        for j, c in enumerate(row):
            antennae_groups[c].append((i, j))
    return grid, list((k, v) for k, v in antennae_groups.items() if k.isalnum())


def vec_sub(a, b):
    return tuple(u - v for u, v in zip(a, b))


def vec_add(a, b):
    return tuple(u + v for u, v in zip(a, b))


def reduce_gcd(t):
    a, b = t
    d = gcd(a, b)
    return a // d, b // d


def part1(grid, groups):
    m = len(grid)
    n = len(grid[0])

    def in_bounds(u, v):
        return 0 <= u < m and 0 <= v < n

    antinodes = set()
    for _, group in groups:
        for a, b in combinations(group, 2):
            diff = vec_sub(b, a)
            antinodes.add(vec_add(b, diff))
            antinodes.add(vec_sub(a, diff))
    return sum(1 for an in antinodes if in_bounds(*an))


def part2(grid, groups):
    m = len(grid)
    n = len(grid[0])

    def in_bounds(t):
        u, v = t
        return 0 <= u < m and 0 <= v < n

    antinodes = set()
    for _, group in groups:
        for a, b in combinations(group, 2):
            diff = reduce_gcd(vec_sub(b, a))
            insert = a
            antinodes.add(insert)
            while in_bounds(insert := vec_add(insert, diff)):
                antinodes.add(insert)
            insert = a
            while in_bounds(insert := vec_sub(insert, diff)):
                antinodes.add(insert)
    return len(antinodes)


if __name__ == "__main__":
    print(part2(*parse(sys.stdin)))
