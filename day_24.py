import sys
from collections import defaultdict


def parse(lines):
    inputs = {}
    while line := next(lines).strip():
        node, val = line.split(": ")
        inputs[node] = int(val)

    gates = {}
    while line := next(lines, "").strip():
        op1, opcode, op2, _arrow, dest = line.split(" ")
        assert opcode in ["AND", "XOR", "OR"]
        gates[dest] = (opcode, op1, op2)
    return inputs, gates


def part1(inputs: dict[str, int], gates: dict[str, tuple[str, str, str]]):
    def compute_opt(dest) -> int:
        if dest in inputs:
            return inputs[dest]
        opcode, op1, op2 = gates.pop(dest)
        op1 = compute_opt(op1)
        op2 = compute_opt(op2)
        match opcode:
            case "AND":
                res = op1 * op2
            case "OR":
                res = max(op1, op2)
            case "XOR":
                res = (op1 + op2) % 2
            case _:
                raise ValueError(f"unhandled op {opcode}")
        inputs[dest] = res
        return res

    for k in list(gates.keys()):
        compute_opt(k)
    assert not gates
    res = 0
    for k, v in sorted(inputs.items(), reverse=True):
        if not k.startswith("z"):
            continue
        res *= 2
        res += v
    return res


def part2(inputs: dict[str, int], gates: dict[str, tuple[str, str, str]]):
    bitwidth = len(inputs) // 2
    assert bitwidth < 100
    assert all(f"{x}{y:02d}" in inputs for x in "xy" for y in range(bitwidth))
    outlinks: defaultdict[str, list[str]] = defaultdict(list)
    for dest, (_, op1, op2) in gates.items():
        outlinks[op1].append(dest)
        outlinks[op2].append(dest)

    swaps = []

    def swap(x, y):
        x_defn = gates.pop(x)
        y_defn = gates.pop(y)
        for xin in x_defn[1:]:
            lst = outlinks[xin]
            lst[lst.index(x)] = y
        for yin in y_defn[1:]:
            lst = outlinks[yin]
            lst[lst.index(y)] = x
        gates[y] = x_defn
        gates[x] = y_defn
        swaps.append(x)
        swaps.append(y)

    # def rename(old, new):
    #     assert old in gates
    #     _opcode, op1, op2 = gates[old]
    #     # this handles i233 = x23 AND x23
    #     for lst in (outlinks[op1], outlinks[op2]):
    #         lst[lst.index(old)] = new
    #     gates[new] = gates.pop(old)
    #     for dest in outlinks[old]:
    #         gates[dest] = tuple(p.replace(old, new) for p in gates[dest])
    #     outlinks[new] = outlinks.pop(old)
    #
    # rename_count = 0
    # renames = {}
    # for k in list(gates.keys()):
    #     if k.startswith("z"):
    #         continue
    #     temp_name = f"i{rename_count:03d}"
    #     rename(k, temp_name)
    #     renames[k] = temp_name
    #     rename_count += 1
    # import pprint; pprint.pprint(gates)

    def find(opcode, op1, op2):
        for poss in outlinks[op1]:
            if gates[poss][0] == opcode:
                if poss in outlinks[op2]:
                    yield poss

    def recovery_find(opcode, op1, op2):
        for poss in outlinks[op1] + outlinks[op2]:
            if gates[poss][0] == opcode:
                yield poss

    def find_one(*args):
        found = list(find(*args))
        if len(found) == 1:
            return found[0]

    # inspect structure of circuit to guess that each full adder
    # is shaped the same and there are no useless/confounding gates.
    # the problem is way harder if these are not true
    s0 = find_one("XOR", "x00", "y00")
    assert s0 == "z00"
    c = find_one("AND", "x00", "y00")
    assert c is not None
    for i in range(1, bitwidth):
        s = find_one("XOR", f"x{i:02d}", f"y{i:02d}")
        c_right_half = find_one("AND", f"x{i:02d}", f"y{i:02d}")
        assert s and c_right_half
        # if s and c_right_half:
        #     pass
        # elif not s and not c_right_half:
        #     raise ValueError(
        #         "do not handle simultaneous swap "
        #         "of carry-right and sum-of-inputs"
        #     )
        # elif s:
        #     print("recovering CRH")
        #     other_right_halves = list(
        #         recovery_find("AND", f"x{i:02d}", f"y{i:02d}"),
        #     )
        #     assert other_right_halves, (
        #         "do not handle both inputs to CRH being swapped"
        #     )
        #     wrong_inputs = [
        #         i
        #         for orh in other_right_halves
        #         for i in gates[orh][1:]
        #         if i not in {f"x{i:02d}", f"y{i:02d}"}
        #     ]
        #     assert len(wrong_inputs) == 1, "only handle one wrong input to CR"
        #     c_right_half = wrong_inputs[0]
        # elif c_right_half:
        #     print("recovering S")
        #     other_sums = list(
        #         recovery_find("AND", f"x{i:02d}", f"y{i:02d}"),
        #     )
        #     assert other_sums, "do not handle both inputs to S being swapped"
        #     wrong_inputs = [
        #         i
        #         for os in other_sums
        #         for i in gates[os][1:]
        #         if i not in {f"x{i:02d}", f"y{i:02d}"}
        #     ]
        #     assert len(wrong_inputs) == 1, "only handle one wrong input to S"
        #     s = wrong_inputs[0]
        # assert s and c and c_right_half
        z = find_one("XOR", s, c)
        if not z:
            other_zs = list(recovery_find("XOR", s, c))
            assert len(other_zs) == 1
            # guess that exactly one of the inputs to z is correct
            guess_z = other_zs[0]
            present_arg = next(
                arg for arg in gates[guess_z][1:] if arg in {s, c}
            )
            missing_arg = min({s, c}.difference({present_arg}))
            _other_idx, other_arg = next(
                (i, s)
                for i, s in enumerate(gates[guess_z])
                if i > 0 and s != present_arg
            )
            swap(other_arg, missing_arg)
            if s == missing_arg:
                s = other_arg
            if c_right_half == other_arg:
                c_right_half = missing_arg
            z = guess_z

        if z != f"z{i:02d}":
            print(f"swapping z{i:02d} with {z}")
            swap(z, f"z{i:02d}")
            if c_right_half == f"z{i:02d}":
                c_right_half = z
            z = f"z{i:02d}"
        c_left_half = find_one("AND", s, c)
        assert c_left_half
        c = find_one("OR", c_left_half, c_right_half)
        if not c:
            print(c_left_half, c_right_half)
            print(list(recovery_find("OR", c_left_half, c_right_half)))
    return ",".join(sorted(swaps))


if __name__ == "__main__":
    print(part2(*parse(sys.stdin)))
