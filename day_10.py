from typing import List
import sys


def parse(lines):
    out = []
    for line in lines:
        out.append([int(c) for c in line.strip()])
    return (out,)


def part1(grid: List[List[int]]):
    start = max(max(r) for r in grid)
    dp = [
        [set([(i, j) for _ in range(1) if c == start]) for j, c in enumerate(r)]
        for i, r in enumerate(grid)
    ]
    ans = 0
    for height in range(start, -1, -1):
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if grid[i][j] == height:
                    for di, dj in ((-1, 0), (1, 0), (0, 1), (0, -1)):
                        if (
                            0 <= i + di < len(grid)
                            and 0 <= j + dj < len(grid)
                            and grid[i + di][j + dj] == height + 1
                        ):
                            dp[i][j].update(dp[i + di][j + dj])
                    if height == 0:
                        ans += len(dp[i][j])
    return ans


def part2(grid: List[List[int]]):
    start = max(max(r) for r in grid)
    dp = [
        [int(c == start) for j, c in enumerate(r)] for i, r in enumerate(grid)
    ]
    ans = 0
    for height in range(start, -1, -1):
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if grid[i][j] == height:
                    for di, dj in ((-1, 0), (1, 0), (0, 1), (0, -1)):
                        if (
                            0 <= i + di < len(grid)
                            and 0 <= j + dj < len(grid)
                            and grid[i + di][j + dj] == height + 1
                        ):
                            dp[i][j] += dp[i + di][j + dj]
                    if height == 0:
                        ans += dp[i][j]
    return ans


if __name__ == "__main__":
    print(part2(*parse(sys.stdin)))
