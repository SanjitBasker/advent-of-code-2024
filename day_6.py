import sys
from contextlib import contextmanager


def parse(lines):
  matches = [[(c == ".", c == "^") for c in line.strip()] for line in lines]
  return [[m[0] for m in row] for row in matches], (
    max(
      range(0, len(matches)), key=lambda i: int(any(m[1] for m in matches[i]))
    ),
    max(
      range(0, len(matches[0])),
      key=lambda i: int(any(m[i][1] for m in matches)),
    ),
  )


def part1(traversable, start):
  traversable[start[0]][start[1]] = True
  direction = (-1, 0)

  def turn(direction):
    return (direction[1], -direction[0])

  def in_bounds(i, j):
    return 0 <= i < len(traversable) and 0 <= j < len(traversable[0])

  pos = start
  seen = set((pos,))  # pos
  while True:
    match tuple(u + v for u, v in zip(pos, direction)):
      case (x, y) as next_pos:
        if (ib := in_bounds(x, y)) and traversable[x][y]:
          pos = next_pos
          seen.add(pos)
        elif ib:
          direction = turn(direction)
        else:
          return len(seen)
      case _:
        print("bad!")


def part2(traversable, start):
  traversable[start[0]][start[1]] = True

  def turn(direction):
    return (direction[1], -direction[0])

  def in_bounds(i, j):
    return 0 <= i < len(traversable) and 0 <= j < len(traversable[0])

  def continue_simulation(start, direction, steps) -> bool:
    pos = start
    seen = set(steps)
    loop = None
    while loop is None:
      for _ in range(4):
        match tuple(u + v for u, v in zip(pos, direction)):
          case (x, y) as tentative_next_pos:
            if not (ib := in_bounds(x, y)):
              break
            elif not traversable[x][y]:
              direction = turn(direction)
              continue
            else:
              break
      else:
        print("infinite loop on a single spot, seems sus")
      if (pos, direction) in seen:
        loop = True
      elif ib:
        seen.add((pos, direction))
        steps.append((pos, direction))
        pos = tentative_next_pos
      else:
        seen.add((pos, direction))
        steps.append((pos, direction))
        loop = False
    return loop

  @contextmanager
  def temp_obstacle(i, j):
    traversable[i][j] = False
    yield
    traversable[i][j] = True

  steps = []
  assert continue_simulation(start, (-1, 0), steps) is False

  ans = set()
  seen = set((start,))
  # only put obstacles in places we go
  for i in range(len(steps) - 1):
    next_pos = steps[i + 1][0]  # propose putting an obstacle here
    if next_pos in seen or next_pos in ans:
      continue
    else:
      seen.add(next_pos)
    with temp_obstacle(*next_pos):
      temp = steps[:i]
      if continue_simulation(*steps[i], temp):
        ans.add(next_pos)
  return len(ans)


if __name__ == "__main__":
  print(part2(*parse(sys.stdin)))
