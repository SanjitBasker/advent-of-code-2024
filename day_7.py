import sys


def parse(lines):
    def parse_line(line):
        target, found, inputs = line.partition(": ")
        assert found
        return int(target), [int(i) for i in inputs.split(" ")]

    return ([parse_line(line.strip()) for line in lines],)


def apply_op(left, right, op):
    # print(f"applying {left} {op} {right}")
    if left == None:
        return right
    elif op == "*":
        return left * right
    elif op == "|":
        return int(str(left) + str(right))
    else:
        return left + right


def search(target, nums, opcodes):
    ops = [("+", None)]

    def dfs():
        last = ops[-1][-1]
        if len(ops) == len(nums) + 1:
            return last == target
        elif last is not None and last > target:
            return False
        else:
            for op in opcodes:
                ops.append((op, apply_op(last, nums[len(ops) - 1], op)))
                if dfs():
                    return True
                ops.pop()
            return False

    return dfs()


def part1(equations):
    ans = 0
    for target, nums in equations:
        if search(target, nums, "+*"):
            ans += target
    return ans


def part2(equations):
    ans = 0
    for target, nums in equations:
        if search(target, nums, "+*|"):
            ans += target
    return ans


if __name__ == "__main__":
    print(part2(*parse(sys.stdin)))
