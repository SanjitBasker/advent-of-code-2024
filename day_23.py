import itertools
from collections import defaultdict
import sys


def parse(lines):
    adj_lst = defaultdict(set)
    for line in lines:
        u, v = line.strip().split("-")
        adj_lst[u].add(v)
        adj_lst[v].add(u)
    return (adj_lst,)


def part1(adj_lst):
    ans = 0
    for u, v, w in itertools.combinations(list(adj_lst.keys()), 3):
        if (
            v in adj_lst[u]
            and w in adj_lst[v]
            and u in adj_lst[w]
            and any(x.startswith("t") for x in [u, v, w])
        ):
            ans += 1
    return ans


def part2(adj_lst):
    cliques = set(tuple([u, v]) for u, vs in adj_lst.items() for v in vs)
    while cliques:
        next_cliques = set()
        for c in cliques:
            for w, ns in adj_lst.items():
                if w in c:
                    continue
                if all(v in ns for v in c):
                    next_cliques.add(c.union([w]))
        if not next_cliques:
            break
        else:
            cliques = next_cliques
    return ",".join(sorted(next(iter(cliques))))


if __name__ == "__main__":
    print(part2(*parse(sys.stdin)))
