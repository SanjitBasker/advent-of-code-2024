import sys
import itertools


def parse(lines):
    locks = []
    keys = []

    def groups():
        acc = []
        for line in lines:
            line = line.strip()
            if acc and not line:
                yield acc
                acc = []
            else:
                acc.append(line)
        if acc:
            yield acc

    for group in groups():
        if all(c == "#" for c in group[0]):
            dest = locks
        else:
            dest = keys
        dest.append(
            tuple(
                sum(1 if c == "#" else 0 for c in column)
                for column in zip(*itertools.chain(group))
            )
        )
    return len(group), locks, keys


def part1(height, locks, keys):
    return len(
        [
            None
            for lock in locks
            for key in keys
            if all(l + k <= height for l, k in zip(lock, key))
        ]
    )


def part2():
    return ()


if __name__ == "__main__":
    print(part1(*parse(sys.stdin)))
