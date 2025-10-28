import sys
import itertools
from typing import Callable, Generator, Literal
from functools import partial

NUMERIC_PAD = {
    c: (i, j)
    for i, s in enumerate(
        [
            "789",
            "456",
            "123",
            "x0A",
        ]
    )
    for j, c in enumerate(s)
}

DIRECTIONAL_PAD = {
    (0, 1): (1, 2),
    (0, -1): (1, 0),
    (1, 0): (1, 1),
    (-1, 0): (0, 1),
    "A": (0, 2),
    "x": (0, 0),
}


class Router[Action]:
    def __init__(
        self,
        name,
        positions: dict[Action, tuple[int, int]],
        cost: Callable[[tuple[int, int], tuple[int, int]], int],
    ) -> None:
        self.name = name
        self.positions = positions
        self.cost = cost
        self.cache: dict[tuple[Action, Action], int] = dict()

    def route(self, curr_token: Action, next_token: Action) -> int:
        if curr_token == next_token:
            return 1
        if (curr_token, next_token) in self.cache:
            return self.cache[(curr_token, next_token)]
        x1, y1 = self.positions[curr_token]
        x2, y2 = self.positions[next_token]
        changes = []
        # changing x then y is always safe
        if dx := x2 - x1:
            changes += [(abs(dx) // dx, 0) for _ in range(abs(dx))]
        if dy := y2 - y1:
            changes += [(0, abs(dy) // dy) for _ in range(abs(dy))]
        c = min(
            c
            for p in itertools.permutations(changes)
            if (c := self.cost_of_sequence_of_moves((x1, y1), p)) is not None
        )

        self.cache[(curr_token, next_token)] = c
        return c

    def cost_of_sequence_of_moves(self, start, seq):
        p: Action = "A"
        pos = start
        cost = 0
        for s in seq:
            cost += self.cost(p, s)
            p = s
            pos = (pos[0] + s[0], pos[1] + s[1])
            if pos == self.positions["x"]:
                return None
        cost += self.cost(p, "A")
        return cost


def parse(lines):
    return ([line.strip() for line in lines if line.strip()],)


def part1(lines):
    human = Router("human", DIRECTIONAL_PAD, cost=lambda *args: 1)
    middle_controller = Router("middle", DIRECTIONAL_PAD, human.route)
    last_controller = Router("final", NUMERIC_PAD, middle_controller.route)
    total = 0
    for line in lines:
        route = 0
        prev = "A"
        for c in line:
            route += last_controller.route(prev, c)
            prev = c
        total += route * int(line[:-1])
    return total


def part2(lines):
    prev = Router("", DIRECTIONAL_PAD, cost=lambda *args: 1)
    for _ in range(24):
        prev = Router("", DIRECTIONAL_PAD, prev.route)
    last_controller = Router("", NUMERIC_PAD, cost=prev.route)
    total = 0
    for line in lines:
        route = 0
        prev = "A"
        for c in line:
            route += last_controller.route(prev, c)
            prev = c
        total += route * int(line[:-1])
    return total


if __name__ == "__main__":
    print(part2(*parse(sys.stdin)))
