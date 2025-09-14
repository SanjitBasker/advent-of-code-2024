import sys
from collections import deque
from itertools import chain


def parse(lines):
    return (list(list(line.strip()) for line in lines),)


def neighbors(i, j, grid):
    for di, dj in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        if 0 <= i + di < len(grid) and 0 <= j + dj < len(grid[i + di]):
            yield (i + di, j + dj)


def part1(grid):
    connected_components = [[None for _ in row] for row in grid]
    areas = []
    perims = []
    comp_id = 0
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if connected_components[i][j] is not None:
                continue
            areas.append(0)
            perims.append(0)
            found = deque([(i, j)])
            while found:
                ii, jj = found.pop()
                if connected_components[ii][jj] is not None:
                    continue
                connected_components[ii][jj] = comp_id
                areas[comp_id] += 1
                for iii, jjj in neighbors(ii, jj, grid):
                    if (
                        connected_components[iii][jjj] is None
                        and grid[iii][jjj] == grid[ii][jj]
                    ):
                        found.append((iii, jjj))
            comp_id += 1

    # 2l(w - 1)
    for i in range(len(grid)):
        for j in range(len(grid[i]) - 1):
            if connected_components[i][j] != connected_components[i][j + 1]:
                perims[connected_components[i][j]] += 1
                perims[connected_components[i][j + 1]] += 1
    # 2w(l - 1)
    for i in range(len(grid) - 1):
        for j in range(len(grid[i])):
            if connected_components[i][j] != connected_components[i + 1][j]:
                perims[connected_components[i][j]] += 1
                perims[connected_components[i + 1][j]] += 1
    # 2w
    for i in [0, len(grid) - 1]:
        for j in range(len(grid[i])):
            perims[connected_components[i][j]] += 1
    # 2l
    for i in range(len(grid)):
        for j in [0, len(grid[i]) - 1]:
            perims[connected_components[i][j]] += 1
    return sum(a * p for a, p in zip(areas, perims))


def get(grid, i, j):
    if 0 <= i < len(grid) and 0 <= j < len(grid[i]):
        return grid[i][j]
    else:
        return None


def part2(grid):
    connected_components = [[None for _ in row] for row in grid]
    areas = []
    perims = []
    comp_id = 0
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if connected_components[i][j] is not None:
                continue
            areas.append(0)
            perims.append(
                (
                    (
                        [[] for _ in range((len(grid)))],
                        [[] for _ in range((len(grid)))],
                        [[] for _ in range((len(grid[0])))],
                        [[] for _ in range((len(grid[0])))],
                    )
                )
            )
            found = deque([(i, j)])
            while found:
                ii, jj = found.pop()
                if connected_components[ii][jj] is not None:
                    continue
                connected_components[ii][jj] = comp_id
                areas[comp_id] += 1
                for iii, jjj in neighbors(ii, jj, grid):
                    if (
                        connected_components[iii][jjj] is None
                        and grid[iii][jjj] == grid[ii][jj]
                    ):
                        found.append((iii, jjj))
            comp_id += 1

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            cc = connected_components[i][j]
            for di, book in ((-1, 0), (1, 1)):
                neighbor = get(connected_components, i + di, j)
                if neighbor != cc:
                    perims[cc][book][i].append(j)
            for dj, book in ((-1, 2), (1, 3)):
                neighbor = get(connected_components, i, j + dj)
                if neighbor != cc:
                    perims[cc][book][j].append(i)

    count_perims = []
    for p in perims:
        count_perims.append(0)
        for q in chain(*p):
            if not q:
                continue
            q.sort()
            assert len(set(q)) == len(q)
            last = None
            for i in q:
                if last is not None and last + 1 == i:
                    last += 1
                else:
                    count_perims[-1] += 1
                    last = i
    return sum(a * p for a, p in zip(areas, count_perims))


if __name__ == "__main__":
    print(part2(*parse(sys.stdin)))
