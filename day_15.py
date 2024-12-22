import enum
import sys
from bisect import bisect_right
from dataclasses import dataclass
from functools import total_ordering
from typing import Iterable, List, Literal, Tuple, Optional

from sortedcontainers import SortedDict


@total_ordering
@enum.unique
class Space(enum.Enum):
  WALL = "#"
  FREE = "."
  BOX = "O"

  def __lt__(self, other):
    if self.__class__ is other.__class__:
      return self.value < other.value
    return NotImplemented


TheOnlyUsefulType = SortedDict[int, Tuple[Space, int]]


@total_ordering
@enum.unique
class Direction(enum.Enum):
  RIGHT = (0, 1)
  LEFT = (0, -1)
  UP = (-1, 0)
  DOWN = (1, 0)

  def __lt__(self, other):
    if self.__class__ is other.__class__:
      return self.value < other.value
    return NotImplemented


def parse(lines):
  start = None
  grid = []
  while l := next(lines).strip():
    row = list(l)
    if any(c == "@" for c in row):
      i = row.index("@")
      start = (len(grid), i)
      row[i] = Space.FREE.value
    grid.append([Space(c) for c in row])
  action_map = {
    "<": Direction.LEFT,
    ">": Direction.RIGHT,
    "^": Direction.UP,
    "v": Direction.DOWN,
  }
  actions = []
  for line in lines:
    if line.strip():
      actions.extend(action_map[c] for c in line.strip())
    else:
      break
  return grid, start, actions


def gen_max(y: int):
  return (y, (max(list(Space)), float("inf")))


def replace(
  sd: TheOnlyUsefulType,
  i: int,
  s: Space,
  expected: Space | None = None,
):
  """
  Replace a single unit of space at a specific index in a space partitioning system.

  This function modifies the given SortedDict in place, replacing the space type
  at the specified index. It handles various cases including splitting existing
  spaces and merging with adjacent spaces of the same type.

  :param sd: A SortedDict representing the space partitioning system.
             Keys are integers representing start indices of spaces.
             Values are tuples (Space, int) where Space is the type of space
             and int is the end index (exclusive) of that space.
  :param i: The specific index at which to replace the space type.
  :param s: The new Space type to be inserted at index i.
  :param expected: Optional. If provided, asserts that the current Space at
                   index i matches this expected Space.

  :raises AssertionError: If the expected Space doesn't match the current Space,
                          or if the index i is not within any existing space range.

  :return: None. The function modifies the input SortedDict in place.

  Note:
  - The function replaces exactly one unit of space at index i.
  - If the new space type is the same as the current type, no change is made.
  - The function may split existing spaces or merge with adjacent spaces of the same type.
  - The function assumes that i is always within an existing range in the SortedDict.

  """
  items = sd.items()
  j = bisect_right(items, gen_max(i)) - 1
  start, (present, finish) = items[j]
  if expected:
    assert present == expected
  assert start <= i < finish

  if present == s:
    return

  left_merge = (
    start == i and 0 <= j - 1 and (prev_item := items[j - 1])[1][0] == s
  )
  right_merge = (
    i + 1 == finish
    and j + 1 < len(items)
    and (next_item := items[j + 1])[1][0] == s
  )

  if left_merge and right_merge:
    prev_start = prev_item[0]
    next_fin = next_item[1][1]
    sd[prev_start] = (s, next_fin)
    del sd[start]
    del sd[start + 1]
  elif left_merge:
    prev_start = prev_item[0]
    sd[prev_start] = (s, i + 1)
    if i + 1 < finish:
      sd[i + 1] = sd[i]
    del sd[i]
  elif right_merge:
    next_fin = next_item[1][1]
    if start < i:
      sd[start] = (present, i)
    sd[i] = (s, next_fin)
    del sd[i + 1]
  elif start == i and i + 1 == finish:
    sd[start] = (s, finish)
  elif start == i:
    sd[start + 1] = items[j][1]
    sd[start] = (s, start + 1)
  elif i + 1 == finish:
    sd[start] = (present, i)
    sd[i] = (s, finish)
  else:
    sd[start] = (present, i)
    sd[i] = (s, i + 1)
    sd[i + 1] = (present, finish)


def move(u: Tuple[int, int], v: Tuple[int, int]) -> Tuple[int, int]:
  return tuple(x + y for x, y in zip(u, v))


def pprint(
  rows: List[TheOnlyUsefulType],
  cols: List[TheOnlyUsefulType],
  wide: bool = False,
) -> Tuple[str, str]:
  def collect(group: TheOnlyUsefulType) -> List[str]:
    ans: List[str] = []
    for item in group.items():
      ans.extend(item[1][0].value for _ in range(item[1][1] - item[0]))
    return ans

  row_chars: Iterable[str] = ("".join(collect(row)) for row in rows)
  col_chars: Iterable[List[str]] = (collect(col) for col in cols)
  transposed_cols = ("".join(a) for a in zip(*list(col_chars)))
  if wide:
    row_chars = (row.replace("OO", "[]") for row in row_chars)
  return "\n".join(row_chars), "\n".join(transposed_cols)


def make_rows_cols(
  grid: List[List[Space]],
) -> Tuple[List[TheOnlyUsefulType], List[TheOnlyUsefulType]]:
  rows: List[TheOnlyUsefulType] = []
  for i in range(len(grid)):
    sd: TheOnlyUsefulType = SortedDict()
    item = None
    for j in range(len(grid[i])):
      if item is None:
        item = (j, grid[i][j])
      elif grid[i][j] != item[1]:
        sd[item[0]] = (item[1], j)
        item = (j, grid[i][j])
    sd[item[0]] = (item[1], len(grid[i]))
    rows.append(sd)

  cols: List[TheOnlyUsefulType] = []
  for j in range(len(grid[0])):
    sd: TheOnlyUsefulType = SortedDict()
    item = None
    for i in range(len(grid)):
      if item is None:
        item = (i, grid[i][j])
      elif grid[i][j] != item[1]:
        sd[item[0]] = (item[1], i)
        item = (i, grid[i][j])
    sd[item[0]] = (item[1], len(grid))
    cols.append(sd)
  return (rows, cols)


def part1(
  grid: List[List[Space]], start: Tuple[int, int], actions: Iterable[Direction]
):
  rows, cols = make_rows_cols(grid)

  pos = start
  for a in actions:
    # s1, s2 = pprint(rows, cols)
    # print(s1)
    # print(s2)
    # print(pos)
    # assert s1 == s2

    # x is the unchanging coordinate
    # to_search is the thing that gets shifted along
    # to_replace is the thing that gets randomly accessed and replaced
    if a.value[0] == 0:
      to_search = rows[pos[0]]
      to_replace = cols
      x, y = pos
    else:
      to_search = cols[pos[1]]
      to_replace = rows
      y, x = pos

    neighbor = bisect_right(to_search.items(), gen_max(y + sum(a.value))) - 1
    neighbor_item = to_search.items()[neighbor]
    if neighbor_item[1][0] == Space.FREE:
      pos = move(pos, a.value)
    elif neighbor_item[1][0] == Space.BOX:
      if 0 <= (following := neighbor + sum(a.value)) < len(to_search):
        following_item = to_search.items()[following]
        if following_item[1][0] == Space.FREE:
          if sum(a.value) == 1:
            box_dest_coord = neighbor_item[1][1]
          elif sum(a.value) == -1:
            box_dest_coord = neighbor_item[0] - 1
          push_row_of_boxes(to_search, neighbor, sum(a.value))
          replace(to_replace[y + sum(a.value)], x, Space.FREE, Space.BOX)
          replace(to_replace[box_dest_coord], x, Space.BOX, Space.FREE)
          pos = move(pos, a.value)

  ans = 0
  for i, row in enumerate(rows):
    for item in row.items():
      if item[1][0] == Space.BOX:
        ans += (
          100 * i * (item[1][1] - item[0])
          + (item[0] + item[1][1] - 1) * (item[1][1] - item[0]) // 2
        )
  return ans


def push_row_of_boxes(sd: TheOnlyUsefulType, j: int, direction: Literal[-1, 1]):
  """
  Does what it says on the tin, i'm too lazy to ask gen AI to write a docstring
  """
  items = sd.items()
  start, (present, finish) = items[j]
  assert present == Space.BOX and 0 < j < len(items) - 1
  squash_item = items[j + direction]
  expand_item = items[j - direction]
  assert squash_item[1][0] == Space.FREE
  if direction == -1:
    del sd[start]
    del sd[squash_item[0]]
    if (kill_squash := squash_item[1][1] == squash_item[0] + 1) and (
      prior_item := items[j - 2]
    )[1][0] == Space.BOX:
      sd[prior_item[0]] = (present, finish - 1)
    elif kill_squash:
      sd[start - 1] = (Space.BOX, finish - 1)
    else:
      sd[squash_item[0]] = (Space.FREE, start - 1)
      sd[start - 1] = (Space.BOX, finish - 1)
    del sd[expand_item[0]]
    sd[expand_item[0] - 1] = expand_item[1]
  else:
    del sd[start]
    del sd[squash_item[0]]
    if (kill_squash := squash_item[1][1] == squash_item[0] + 1) and (
      following_item := items[j]
    )[1][0] == Space.BOX:
      # merge with following
      sd[start + 1] = following_item[1]
      del sd[following_item[0]]
    elif kill_squash:
      sd[start + 1] = (Space.BOX, finish + 1)
    else:
      sd[start + 1] = (Space.BOX, finish + 1)
      sd[finish + 1] = squash_item[1]
    sd[expand_item[0]] = (expand_item[1][0], start + 1)


@dataclass(frozen=False)
class MovingBox:
  coords: Tuple[int, int]


def vertical_obstacles(
  rows: List[TheOnlyUsefulType], box: Tuple[int, int], direction: Literal[-1, 1]
) -> Optional[List[MovingBox]]:
  row, col = box
  if 0 <= (row + direction) < len(rows):
    next_row = rows[row + direction]
    items = next_row.items()
    start, (space, finish) = items[bisect_right(items, gen_max(col)) - 1]
    assert start <= col < finish
    if finish == start + 1:
      space2 = rows[row + direction][start + 1][0]
    else:
      space2 = space
    match (space, space2):
      case (Space.WALL, _) | (_, Space.WALL):
        return None
      case (Space.FREE, Space.FREE):
        return []
      case (Space.FREE, Space.BOX):
        return [(row + direction, col + 1)]
      case (Space.BOX, Space.FREE):
        return [(row + direction, col - 1)]
      case (Space.BOX, Space.BOX):
        if (col - start) % 2 == 0:
          return [((row + direction), col)]
        else:
          return [
            ((row + direction), col - 1),
            ((row + direction), col + 1),
          ]
      case _:
        assert False
  assert False


def compute_vertical_moves(
  rows: List[TheOnlyUsefulType],
  original_box: Tuple[int, int],
  direction: Literal[-1, 1],
) -> List[Tuple[int, int]]:
  ans = []
  ans.append(original_box)
  finished = 0
  while finished < len(ans):
    box = ans[finished]
    obstacles = vertical_obstacles(rows, box, direction)
    if obstacles is None:
      return []
    else:
      for obs in obstacles:
        if obs != ans[-1]:
          ans.append(obs)
    finished += 1
  return ans


def part2():
  return ()


if __name__ == "__main__":
  print(part1(*parse(sys.stdin)))
