import sys
import itertools
import heapq
from dataclasses import dataclass
from collections import defaultdict


def parse(lines):
    rows = list(lines)
    traversable = [[c != "#" for c in r] for r in rows]
    start = next(
        itertools.chain.from_iterable(
            ((i, j) for j, c in enumerate(r) if c == "S")
            for i, r in enumerate(rows)
        )
    )
    end = next(
        itertools.chain.from_iterable(
            ((i, j) for j, c in enumerate(r) if c == "E")
            for i, r in enumerate(rows)
        )
    )
    return traversable, start, end


@dataclass(frozen=True, order=True)
class VisitRecord:
    distance: int
    loc: tuple[int, int]
    arrival_direction: tuple[int, int]

    def serialize(self, n: int):
        return (
            4 * (self.loc[0] * n + self.loc[1])
            + (
                -3 * self.arrival_direction[0]
                + -1 * self.arrival_direction[1]
                + 3
            )
            // 2
        )


def turns(direction):
    x, y = direction
    yield 1000 + 1, -y, x
    yield 1000 + 1, y, -x
    yield 1, x, y


def dijkstra(traversable, start, end):
    visited: list[list[VisitRecord | None]] = [
        [None for _ in r] for r in traversable
    ]
    frontier = [VisitRecord(0, start, (0, 1))]
    heapq.heapify(frontier)
    visited[start[0]][start[1]] = VisitRecord(0, start, (0, 1))
    while frontier:
        vr = heapq.heappop(frontier)
        if vr.loc == end:
            return visited
        x, y = vr.loc
        for ds, dx, dy in turns(vr.arrival_direction):
            visit = VisitRecord(vr.distance + ds, (x + dx, y + dy), (dx, dy))
            if not traversable[visit.loc[0]][visit.loc[1]]:
                continue
            if not visited[visit.loc[0]][visit.loc[1]]:
                visited[visit.loc[0]][visit.loc[1]] = visit
                heapq.heappush(frontier, visit)
    return visited


def part1(traversable, start, end):
    vrs = dijkstra(traversable, start, end)
    dest = vrs[end[0]][end[1]]
    assert dest is not None, "couldn't reach end"
    return dest.distance


def dijkstra4(traversable, start):
    n = len(traversable)

    init_vr = VisitRecord(0, start, (0, 1))
    visited: list[VisitRecord | None] = [None] * (4 * n**2)
    visited[init_vr.serialize(n)] = init_vr
    frontier = [init_vr]
    heapq.heapify(frontier)
    while frontier:
        vr = heapq.heappop(frontier)
        x, y = vr.loc
        for ds, dx, dy in turns(vr.arrival_direction):
            visit = VisitRecord(vr.distance + ds, (x + dx, y + dy), (dx, dy))
            if not traversable[visit.loc[0]][visit.loc[1]]:
                continue
            if (
                not visited[visit.serialize(n)]
                or visited[visit.serialize(n)] > visit
            ):
                visited[visit.serialize(n)] = visit
                heapq.heappush(frontier, visit)
    return visited


def part2(traversable, start, end):
    n = len(traversable)
    vrs = dijkstra4(traversable, start)
    for i in range(n):
        for j in range(n):
            for k in range(4):
                vr = vrs[4 * (n * i + j) + k]
                if vr:
                    assert vr.loc == (i, j)

    def hash_pos(pos):
        return 4 * (n * pos[0] + pos[1])

    start_idx = hash_pos(end)

    dests = vrs[start_idx : start_idx + 4]
    stack = [
        d
        for d in dests
        if d and d.distance == min(filter(None, dests)).distance
    ]
    visited = set(stack)

    def predecessors(vr):
        predecessor_positions = [
            (vr.loc[0] + d * x, vr.loc[1] + d * (1 - x))
            for d in [-1, 1]
            for x in [0, 1]
        ]
        for ppos in predecessor_positions:
            for i in range(4):
                prev_vr = vrs[hash_pos(ppos) + i]
                if prev_vr is None:
                    continue
                turn_penalty = (
                    1000
                    if sum(
                        i * j
                        for i, j in zip(
                            vr.arrival_direction, prev_vr.arrival_direction
                        )
                    )
                    == 0
                    else 0
                )
                forward_distance = prev_vr.distance + 1 + turn_penalty
                assert forward_distance >= vr.distance, (
                    f"vr did not have an optimal distance {prev_vr} {vr}"
                )
                if forward_distance == vr.distance:
                    yield prev_vr

    while stack:
        top = stack.pop()
        for prev_vr in predecessors(top):
            if prev_vr in visited:
                continue
            visited.add(prev_vr)
            stack.append(prev_vr)
    return len(set(vr.loc for vr in visited))


if __name__ == "__main__":
    print(part2(*parse(sys.stdin)))
