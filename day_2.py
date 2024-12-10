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


def part2(lines):
    def fixable(diffs, good):
        if all(d in good for d in diffs[1:-1]) and (
            diffs[0] in good or diffs[-1] in good
        ):
            return True
        else:
            bad = [i for i, d in enumerate(diffs) if d not in good]
            if len(bad) == 1:
                (b,) = bad
                return (b > 0 and diffs[b - 1] + diffs[b] in good) or (
                    b < len(diffs) - 1 and diffs[b] + diffs[b + 1] in good
                )
            elif len(bad) == 2:
                return bad[1] - bad[0] == 1 and diffs[bad[0]] + diffs[bad[1]] in good
            else:
                return False

    # i just came up with this nice little syntax
    return sum(
        int(fixable(diffs, {1, 2, 3}) or fixable(diffs, {-1, -2, -3}))
        for report in lines
        for diffs in ([p - q for p, q in pairwise(report)],)
    )


if __name__ == "__main__":
    print(part2(*parse()))
