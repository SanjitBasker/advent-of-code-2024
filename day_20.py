import sys


def parse(lines):
    lines = [sline for line in lines if (sline := line.strip())]
    return (list(list(line) for line in lines),)


DIRECTIONS = [(-1, 0), (1, 0), (0, 1), (0, -1)]
SKIP_MIN = int(sys.argv[-1])
CHEAT_DURATION = int(sys.argv[-2])


def get_path(grid):
    i, j = next(
        (
            (i, j)
            for i, row in enumerate(grid)
            for j, c in enumerate(row)
            if c == "S"
        )
    )
    path = []
    last_dx = 0
    last_dy = 0
    while grid[i][j] != "E":
        path.append((i, j))
        for dx, dy in DIRECTIONS:
            if grid[i + dx][j + dy] == "#":
                continue
            elif dx + last_dx == 0 and dy + last_dy == 0:
                continue
            i += dx
            j += dy
            last_dx = dx
            last_dy = dy
            break
    path.append((i, j))
    return path


def reachable_in_2(c1, c2):
    x1, y1 = c1
    x2, y2 = c2
    for dx1, dy1 in DIRECTIONS:
        for dx2, dy2 in DIRECTIONS:
            if x1 + dx1 + dx2 == x2 and y1 + dy1 + dy2 == y2:
                return True
    return False


def cheat_dist(c1, c2):
    x1, y1 = c1
    x2, y2 = c2
    dist = abs(x1 - x2) + abs(y1 - y2)
    if dist <= CHEAT_DURATION:
        return dist
    return float("inf")


def part1(grid):
    path = get_path(grid)
    count = 0
    for i, c in enumerate(path):
        # idea: instead of iterating through the entire path we can maintain the
        # future entries (x, y, idx_on_path) in a list of lists indexed by x + y
        # and check the entries that are within CHEAT_DURATION
        for j, c2 in enumerate(path[i:]):
            if j - cheat_dist(c, c2) >= SKIP_MIN:
                count += 1
    return count


def part2():
    return ()


if __name__ == "__main__":
    print(part1(*parse(sys.stdin)))
