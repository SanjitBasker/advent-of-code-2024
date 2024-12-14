from typing import List, Tuple, Generator

import sys
from dataclasses import dataclass
from itertools import chain


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


@dataclass
class UpdatableBlock:
  block: Tuple[int, int]  # offset, len
  updates: List["UpdatableBlock"]  # must use these instead if available


def find_blocks(
  l: List[UpdatableBlock], min_length: int = 0, stop_loc: int = 10**5
) -> Generator[UpdatableBlock]:
  for b in l:
    if b.block[0] > stop_loc:
      return
    elif b.updates:
      for bb in find_blocks(b.updates):
        yield bb
    elif b.block[1] >= min_length:
      yield b


def collapse(blocks: List[Tuple[int | None, int]]):
  out = []
  for b in blocks:
    if b[1] == 0:
      continue
    elif out and out[-1][0] == b[0]:
      out[-1][1] += b[1]
    else:
      out.append(b)
  return out


def part2(blocks: List[Tuple[int | None, int]]):
  print(blocks)
  blocks = collapse(blocks)
  print(blocks)
  empties: List[UpdatableBlock] = []
  fulls: List[Tuple[int, int, int]] = []  # id, source start, len
  total = 0
  for b in blocks:
    if b[0] is None:
      empties.append(UpdatableBlock((total, b[1]), []))
    else:
      fulls.append((b[0], total, b[1]))
    total += b[1]
  print(empties)
  print(fulls)
  spots = [find_blocks(empties, i) for i in range(1, 10)]
  destinations = []  # id, destination start, len
  for f in fulls[::-1]:
    f_id, f_start, f_len = f
    print(spots[f_len - 1])
    insertion_pt = next(spots[f_len - 1] or [None], None)
    if insertion_pt is not None:
      insertion_start, insertion_avail = insertion_pt.block
      if insertion_start >= f_start:
        destinations.append((f_id, f_start, f_len))
        spots[f_len - 1] = []
        continue
      assert insertion_start <= f_start
      assert insertion_avail >= f_len
      insertion_pt.updates.append(
        UpdatableBlock((insertion_start + f_len, insertion_avail - f_len), [])
      )
      destinations.append((f_id, insertion_start, f_len))

      # for i, it in enumerate(spots):
      #   if (spot := next(it, None)) is not None:
      #     spot_start, spot_avail = spot.block
      #     if insertion_start <= spot_start < insertion_start + f_len:
      #       if f_len + (i + 1) <= insertion_avail:
      #         spots[i] = chain(
      #           [
      #             UpdatableBlock(
      #               (
      #                 insertion_start + f_len,
      #                 insertion_avail - f_len,
      #               ),
      #               [],
      #             )
      #           ],
      #           it,
      #         )
      #       else:
      #         # we discarded it for them
      #         pass
      #     else:
      #       # full rollback
      #       spots[i] = chain([spot], it)
    else:
      destinations.append((f_id, f_start, f_len))
  ans = 0
  for d_id, d_start, d_len in destinations:
    for _ in range(d_len):
      ans += d_id * d_start
      d_start += 1
  return ans


if __name__ == "__main__":
  print(part2(*parse(sys.stdin)))
