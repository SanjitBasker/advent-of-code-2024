from typing import List, Tuple, Iterable
import sys
import enum
from bisect import bisect_left, bisect_right
from sortedcontainers import SortedDict
from functools import total_ordering


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


def find(
  sd, i, d
) -> Tuple[
  Tuple[int, Tuple[int, Space]],
  Tuple[int, Tuple[int, Space]],
]:
  items = sd.items()
  j = bisect_left(items, (i, (i, min(list(Space)))))
  assert items[j][0] <= i < items[j][1][1]
  return items[j], items[j + d]


def gen_max(y: int):
  return (y, (max(list(Space)), float("inf")))


def replace(
  sd: SortedDict[int, Tuple[Space, int]],
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
    print(f"merging both, {prev_item=} {next_item=}")
    prev_start = prev_item[0]
    next_fin = next_item[1][1]
    sd[prev_start] = (s, next_fin)
    del sd[start]
    del sd[start + 1]
  elif left_merge:
    print("merging left")
    prev_start = prev_item[0]
    sd[prev_start] = (s, i + 1)
    if i + 1 < finish:
      sd[i + 1] = sd[i]
    del sd[i]
  elif right_merge:
    print("merging right")
    next_fin = next_item[1][1]
    if start < i:
      sd[start] = (present, i)
    sd[i] = (s, next_fin)
    del sd[i + 1]
  elif start == i and i + 1 == finish:
    print("size=1")
    sd[start] = (s, finish)
  elif start == i:
    print("at start")
    sd[start + 1] = items[j][1]
    sd[start] = (s, start + 1)
  elif i + 1 == finish:
    print("at end")
    sd[start] = (present, i)
    sd[i] = (s, finish)
  else:
    print("in middle")
    sd[start] = (present, i)
    sd[i] = (s, i + 1)
    sd[i + 1] = (present, finish)


def push(sd, start, finish): ...


def move(u: Tuple[int, int], v: Tuple[int, int]) -> Tuple[int, int]:
  return tuple(x + y for x, y in zip(u, v))


def pprint(
  rows: List[SortedDict[int, Tuple[Space, int]]],
  cols: List[SortedDict[int, Tuple[Space, int]]],
) -> Tuple[str, str]:
  def collect(group: SortedDict[int, Tuple[Space, int]]) -> List[str]:
    ans: List[str] = []
    for item in group.items():
      ans.extend(item[1][0].value for _ in range(item[1][1] - item[0]))
    return ans

  row_chars: Iterable[str] = ("".join(collect(row)) for row in rows)
  col_chars: Iterable[List[str]] = (collect(col) for col in cols)
  transposed_cols = ("".join(a) for a in zip(*list(col_chars)))
  return "\n".join(row_chars), "\n".join(transposed_cols)


def part1(
  grid: List[List[Space]], start: Tuple[int, int], actions: Iterable[Direction]
):
  rows: List[SortedDict[int, Tuple[Space, int]]] = []
  for i in range(len(grid)):
    sd: SortedDict[int, Tuple[Space, int]] = SortedDict()
    item = None
    for j in range(len(grid[i])):
      if item is None:
        item = (j, grid[i][j])
      elif grid[i][j] != item[1]:
        sd[item[0]] = (item[1], j)
        item = (j, grid[i][j])
    sd[item[0]] = (item[1], len(grid[i]))
    rows.append(sd)

  cols: List[SortedDict[int, Tuple[Space, int]]] = []
  for j in range(len(grid[0])):
    sd: SortedDict[int, Tuple[Space, int]] = SortedDict()
    item = None
    for i in range(len(grid)):
      if item is None:
        item = (i, grid[i][j])
      elif grid[i][j] != item[1]:
        sd[item[0]] = (item[1], i)
        item = (i, grid[i][j])
    sd[item[0]] = (item[1], len(grid))
    cols.append(sd)

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
          replace(to_search, y + sum(a.value), Space.FREE, Space.BOX)
          replace(to_search, box_dest_coord, Space.BOX, Space.FREE)
          replace(to_replace[y + sum(a.value)], x, Space.FREE, Space.BOX)
          replace(to_replace[box_dest_coord], x, Space.BOX, Space.FREE)
          pos = move(pos, a.value)
    else:
      print("Stuck")

  ans = 0
  for i, row in enumerate(rows):
    for item in row.items():
      if item[1][0] == Space.BOX:
        ans += (
          100 * i * (item[1][1] - item[0])
          + (item[0] + item[1][1] - 1) * (item[1][1] - item[0]) // 2
        )
  return ans


def part2():
  return ()


if __name__ == "__main__":
  print(part1(*parse(sys.stdin)))
