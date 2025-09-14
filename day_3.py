import sys
import re


def merge_streams(iters, key):
    sentinel = []
    nexts = [(n, i) for i in iters if (n := next(i, sentinel)) is not sentinel]
    while nexts:
        n, i = nexts.pop(min(range(len(nexts)), key=lambda i: key(nexts[i][0])))
        yield n
        if (n := next(i, sentinel)) is not sentinel:
            nexts.append((n, i))


def parse(lines):
    return ("\n".join(lines),)


def part1(program):
    pat = re.compile(r"mul\(([0-9]{1,3}),([0-9]{1,3})\)")
    return sum(
        int(m.group(1)) * int(m.group(2)) for m in re.finditer(pat, program)
    )


def part2(program):
    mul_pat = re.compile(r"mul\(([0-9]{1,3}),([0-9]{1,3})\)")
    do_pat = re.compile(r"do\(\)")
    dont_pat = re.compile(r"don't\(\)")
    do = True
    ans = 0
    for event, match in merge_streams(
        [
            (("DO", match) for match in re.finditer(do_pat, program)),
            (("DONT", match) for match in re.finditer(dont_pat, program)),
            (("MUL", match) for match in re.finditer(mul_pat, program)),
        ],
        lambda p: (p[1].start()),
    ):
        if event == "DO":
            do = True
        elif event == "DONT":
            do = False
        elif do:
            ans += int(match.group(1)) * int(match.group(2))
    return ans


if __name__ == "__main__":
    print(part2(*parse(sys.stdin)))
