import sys
from collections import Counter
from itertools import pairwise


def parse():
    return (
        [
            [int(lvl) for lvl in line.strip().split(" ")]
            for line in sys.stdin
            if line.strip()
        ],
    )


def part1(lines):
    def gradual(report):
        diffs = set(p - q for p, q in pairwise(report))
        return all(1 <= d <= 3 for d in diffs) or all(-3 <= d <= -1 for d in diffs)

    return sum(int(gradual(r)) for r in lines)


def part2(left, right):
    rc = Counter(right)
    print(sum(l * rc[l] for l in left))


if __name__ == "__main__":
    print(part1(*parse()))
