import re
import sys
from itertools import batched
import numpy as np
from math import gcd


def parse(lines):
    res = [
        re.compile(r"Button A: X\+(\d+), Y\+(\d+)"),
        re.compile(r"Button B: X\+(\d+), Y\+(\d+)"),
        re.compile(r"Prize: X=(\d+), Y=(\d+)"),
    ]
    groups = batched(
        [l for line in lines if (l := line.strip())],
        3,
    )
    return (
        [
            tuple(
                tuple(int(m) for m in a.match(b).groups((1, 2)))
                for a, b in zip(res, group)
            )
            for group in groups
        ],
    )


def part1(groups):
    ans = 0
    for u, v, target in groups:
        if u[0] * v[1] == u[1] * v[0]:
            vx, vy = target
            for i in range(100):
                if (
                    vx % v[0] == 0
                    and vy % v[1] == 0
                    and 0 <= vx // v[0] == vy // v[1]
                ):
                    ans += i * 3 + vx // v[0]
                    break
                vx -= u[0]
                vy -= u[1]
        else:
            m = np.array([u, v]).T
            t = np.array(target).T
            sol = np.linalg.solve(m, t).T
            cast = np.round(sol).astype(np.int64)
            if np.allclose(m @ cast, t, 0, 0.5) and all(0 <= cast):
                ans += cast @ np.array([3, 1]).T
    return ans


def part2(groups):
    ans = 0
    for u, v, target in groups:
        if u[0] * v[1] == u[1] * v[0]:
            vx, vy = target
            vx += 10000000000000
            vy += 10000000000000
            for i in range(u[0] * v[0]):
                if (
                    vx % v[0] == 0
                    and vy % v[1] == 0
                    and 0 <= vx // v[0] == vy // v[1]
                ):
                    ans += i * 3 + vx // v[0]
                    break
                vx -= u[0]
                vy -= u[1]
        else:
            m = np.array([u, v]).T
            t = np.array(target).T
            t += 10000000000000
            sol = np.linalg.solve(m, t).T
            cast = np.round(sol).astype(np.int64)
            if np.allclose(m @ cast, t, 0, 0.5) and all(0 <= cast):
                ans += cast @ np.array([3, 1]).T
    return ans


if __name__ == "__main__":
    print(part2(*parse(sys.stdin)))
