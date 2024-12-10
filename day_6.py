import sys


def parse(lines):
    matches = [[(c == ".", c == "^") for c in line.strip()] for line in lines]
    return [[m[0] for m in row] for row in matches], (
        max(range(0, len(matches)), key=lambda i: int(any(m[1] for m in matches[i]))),
        max(
            range(0, len(matches[0])), key=lambda i: int(any(m[i][1] for m in matches))
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


def part2():
    return ()


if __name__ == "__main__":
    print(part1(*parse(sys.stdin)))
