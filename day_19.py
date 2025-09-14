import sys


def parse(lines):
    towels = next(lines).strip().split(", ")
    next(lines)
    return towels, [line.strip() for line in lines if line.strip()]


class SmallList:
    def __init__(self, max_concurrent, init):
        self.storage = [init] * max_concurrent

    def __setitem__(self, i, x):
        self.storage[i % len(self.storage)] = x

    def __getitem__(self, i):
        return self.storage[i % len(self.storage)]


def can_make(towels, pattern):
    dp = SmallList(max(len(s) for s in towels) + 1, False)
    dp[0] = True
    for i in range(1, len(pattern) + 1):
        dp[i] = any(
            i >= len(towel)
            and pattern[i - len(towel) : i] == towel
            and dp[i - len(towel)]
            for towel in towels
        )
    return dp[len(pattern)]


def part1(towels, patterns):
    makeable = [can_make(towels, pattern) for pattern in patterns]
    return sum(1 for m in makeable if m)


def count_make(towels, pattern):
    dp = SmallList(max(len(s) for s in towels) + 1, 0)
    dp[0] = 1
    for i in range(1, len(pattern) + 1):
        dp[i] = sum(
            dp[i - len(towel)]
            for towel in towels
            if i >= len(towel) and pattern[i - len(towel) : i] == towel
        )
    return dp[len(pattern)]


def part2(towels, patterns):
    counts = [count_make(towels, pattern) for pattern in patterns]
    return sum(counts)


if __name__ == "__main__":
    print(part2(*parse(sys.stdin)))
