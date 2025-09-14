import sys
from collections import defaultdict


def parse(lines):
    rules = []
    for line in lines:
        if line.strip():
            rules.append(tuple(int(p) for p in line.strip().split("|")))
        else:
            break
    updates = []
    for line in lines:
        if line.strip():
            updates.append(tuple(int(p) for p in line.strip().split(",")))
    return rules, updates


def part1(rules, updates):
    forwards = defaultdict(list)
    for l, r in rules:
        forwards[l].append(r)
    ans = 0
    for update in updates:
        indices = {u: i for i, u in enumerate(update)}
        if all(
            all(indices.get(r, len(update)) >= i for r in forwards[l])
            for i, l in enumerate(update)
        ):
            ans += update[len(update) // 2]
    return ans


def part2(rules, updates):
    forwards = defaultdict(set)
    for l, r in rules:
        forwards[l].add(r)

    ans = 0
    for update in updates:
        indices = {u: i for i, u in enumerate(update)}
        if all(
            all(indices.get(r, len(update)) >= i for r in forwards[l])
            for i, l in enumerate(update)
        ):
            pass
        else:
            slice_forwards = {
                k: forwards[k].intersection(update) for k in update
            }
            ordering = []
            inserted = None
            while slice_forwards:
                next_insert = None
                for k, v in slice_forwards.items():
                    if inserted in v:
                        v.remove(inserted)
                    if not v and not next_insert:
                        next_insert = k
                del slice_forwards[next_insert]
                inserted = next_insert
                ordering.append(next_insert)
            ans += ordering[len(ordering) // 2]
    return ans


if __name__ == "__main__":
    print(part2(*parse(sys.stdin)))
