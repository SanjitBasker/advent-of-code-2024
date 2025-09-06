import sys
from collections import Counter


def parse():
  lines = [line.strip() for line in sys.stdin if line.strip()]
  left = [int(line[: line.find(" ")]) for line in lines]
  right = [int(line[line.rfind(" ") :]) for line in lines]
  return left, right


def part1(left, right):
  assert len(left) == len(right)
  left.sort()
  right.sort()
  return sum(abs(l - r) for l, r in zip(left, right))


def part2(left, right):
  rc = Counter(right)
  return sum(l * rc[l] for l in left)


if __name__ == "__main__":
  print(part2(*parse()))
