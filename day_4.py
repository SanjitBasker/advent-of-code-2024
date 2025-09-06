import sys
import re
from collections import Counter


def parse(lines):
  return ([list(line.strip()) for line in lines],)


def part1(grid):
  n = len(grid)
  m = len(grid[0])

  def get(i, j):
    if 0 <= i < n and 0 <= j < m:
      return grid[i][j]
    else:
      return None

  def search(start, word, direction):
    i, j = start
    di, dj = direction
    for w in word:
      if get(i, j) != w:
        return False
      i += di
      j += dj
    return True

  return sum(
    int(search((i, j), "XMAS", (di, dj)))
    for i in range(n)
    for j in range(m)
    for di in (-1, 0, 1)
    for dj in (-1, 0, 1)
  )


def part2(grid):
  n = len(grid)
  m = len(grid[0])

  def get(i, j):
    if 0 <= i < n and 0 <= j < m:
      return grid[i][j]
    else:
      return None

  def search(start, word, direction):
    i, j = start
    di, dj = direction
    for w in word:
      if get(i, j) != w:
        return False
      i += di
      j += dj
    return True

  mases = Counter(
    (i + di, j + dj)
    for i in range(n)
    for j in range(m)
    for di in (-1, 1)
    for dj in (-1, 1)
    if search((i, j), "MAS", (di, dj))
  )
  return sum(int(v == 2) for v in mases.values())


if __name__ == "__main__":
  print(part2(*parse(sys.stdin)))
