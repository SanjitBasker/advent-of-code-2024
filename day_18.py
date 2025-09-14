import bisect
import itertools
import sys


def parse(lines):
    ints = [[int(p) for p in line.strip().split(",")] for line in lines]
    return ints[0][0], ints[1][0], ints[2:]


def part1(size, time, coords):
    traversable = [[True] * size for _ in range(size)]
    for i, j in coords[:time]:
        traversable[i][j] = False
    # print(traversable)

    def neighbors(p):
        x, y = p
        for dx, dy in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            if (
                0 <= x + dx < size
                and 0 <= y + dy < size
                and traversable[x + dx][y + dy]
            ):
                yield (x + dx, y + dy)

    dest = (size - 1, size - 1)
    dist = 0
    visited = set([(0, 0)])
    level_set = [(0, 0)]
    while level_set:
        if dest in visited:
            return dist

        def visit(p):
            for q in neighbors(p):
                if q not in visited:
                    yield q
                    visited.add(q)

        level_set = list(
            itertools.chain.from_iterable(visit(p) for p in level_set)
        )
        dist += 1


def part2(size, _, coords):
    class C:
        def __len__(self):
            return len(coords)

        def __getitem__(self, i):
            return part1(size, i, coords) or float("inf")

    first_blocker = bisect.bisect_left(C(), float("inf"))
    return coords[first_blocker - 1]


if __name__ == "__main__":
    print(part2(*parse(sys.stdin)))
