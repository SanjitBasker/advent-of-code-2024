from typing import List, Tuple

import sys


def parse(lines):
  line = next(lines).strip()
  ans: List[Tuple[int | None, int]] = []
  next_is_empty = False
  next_id = 0
  for c in line:
    if next_is_empty:
      ans.append((None, int(c)))
    else:
      ans.append((next_id, int(c)))
      next_id += 1
    next_is_empty = not next_is_empty
  return (ans,)


def part1(blocks: List[Tuple[int | None, int]]):
  compacted = []
  left = 0
  right = len(blocks) - 1
  remaining: Tuple[int, None] | Tuple[None, None] | Tuple[None, int] = (
    None,
    None,
  )
  while left < right:
    if (left_id := blocks[left][0]) is not None:
      compacted.append(blocks[left])
      left += 1
      continue
    elif (right_id := blocks[right][0]) is None:
      right -= 1
      continue
    if remaining[0] is not None:
      if remaining[0] > blocks[right][1]:
        compacted.append(blocks[right])
        remaining = (remaining[0] - blocks[right][1], None)
        right -= 1
        continue
      elif remaining[0] < blocks[right][1]:
        compacted.append((right_id, remaining[0]))
        remaining = (None, blocks[right][1] - remaining[0])
        left += 1
        continue
      else:
        compacted.append((right_id, remaining[0]))
        remaining = (None, None)
        left += 1
        right -= 1
        # sus
    elif remaining[1] is not None:
      if remaining[1] > blocks[left][1]:
        compacted.append((right_id, blocks[left][1]))
        remaining = (None, remaining[1] - blocks[left][1])
        left += 1
        continue
      elif remaining[1] < blocks[left][1]:
        compacted.append((right_id, remaining[1]))
        remaining = (blocks[left][1] - remaining[1], None)
        right -= 1
        continue
      else:
        compacted.append((right_id, remaining[1]))
        remaining = (None, None)
        left += 1
        right -= 1
    else:
      if blocks[left][1] < blocks[right][1]:
        compacted.append((right_id, blocks[left][1]))
        remaining = (None, blocks[right][1] - blocks[left][1])
        left += 1
      elif blocks[left][1] > blocks[right][1]:
        compacted.append(blocks[right])
        remaining = (blocks[left][1] - blocks[right][1], None)
        right -= 1
      else:
        compacted.append((right_id, blocks[left][1]))
        left += 1
        right -= 1
  if (
    (left == right)
    and (blocks[left][0] is not None)
    and (r := remaining[0] or remaining[1]) is not None
  ):
    compacted.append((blocks[left][0], r))

  print(compacted)

  cs = 0
  blocks = 0
  for group in compacted:
    block_id, block_size = group
    for _ in range(block_size):
      cs += block_id * blocks
      blocks += 1
  return cs


def part2(blocks: List[Tuple[int | None, int]]):
  return None


if __name__ == "__main__":
  print(part1(*parse(sys.stdin)))
