import sys
import itertools
from dataclasses import dataclass


@dataclass
class InterpreterState:
    ip: int
    registers: list[int]  # len 3
    out: list[int]


@dataclass(frozen=True)
class Register:
    i: int

    def evaluate(self, registers):
        return registers[self.i]

    def __repr__(self):
        return "abc"[self.i]


@dataclass(frozen=True)
class Immediate:
    x: int

    def evaluate(self, _):
        return self.x

    def __repr__(self):
        return str(self.x) + "ul"


@dataclass(frozen=True)
class Adv:
    op: Immediate | Register

    def apply(self, state: InterpreterState):
        state.registers[0] //= 2 ** self.op.evaluate(state.registers)
        state.ip += 1

    def __repr__(self):
        return "a = a >> " + repr(self.op)


@dataclass(frozen=True)
class Bxl:
    op: Immediate

    def apply(self, state: InterpreterState):
        state.registers[1] ^= self.op.evaluate(None)
        state.ip += 1

    def __repr__(self):
        return "b ^= " + repr(self.op)


@dataclass(frozen=True)
class Bst:
    op: Immediate | Register

    def apply(self, state: InterpreterState):
        state.registers[1] = self.op.evaluate(state.registers) % 8
        state.ip += 1

    def __repr__(self):
        return "b = " + repr(self.op) + " % 8"


@dataclass(frozen=True)
class Jnz:
    op: Immediate

    def apply(self, state: InterpreterState):
        if not state.registers[0]:
            state.ip += 1
        else:
            state.ip = self.op.evaluate(None) // 2

    def __repr__(self):
        return "if a: goto " + repr(self.op)


@dataclass(frozen=True)
class Bxc:
    pass

    def apply(self, state: InterpreterState):
        state.registers[1] ^= state.registers[2]
        state.ip += 1

    def __repr__(self):
        return "b ^= c"


@dataclass(frozen=True)
class Out:
    op: Immediate | Register

    def apply(self, state: InterpreterState):
        state.out.append(self.op.evaluate(state.registers) % 8)
        state.ip += 1

    def __repr__(self):
        return "printf " + repr(self.op)


@dataclass(frozen=True)
class Bdv:
    op: Immediate | Register

    def apply(self, state: InterpreterState):
        state.registers[1] = state.registers[0] // 2 ** self.op.evaluate(
            state.registers
        )
        state.ip += 1

    def __repr__(self):
        return "b= a >> " + repr(self.op)


@dataclass(frozen=True)
class Cdv:
    op: Immediate | Register

    def apply(self, state: InterpreterState):
        state.registers[2] = state.registers[0] // 2 ** self.op.evaluate(
            state.registers
        )
        state.ip += 1

    def __repr__(self):
        return "c = a >> " + repr(self.op)


def parse_instr(i, j):
    combos = (
        [Immediate(i) for i in range(4)]
        + [Register(i) for i in range(3)]
        + [None]
    )
    literals = [Immediate(i) for i in range(8)]
    cls = [Adv, Bxl, Bst, Jnz, Bxc, Out, Bdv, Cdv][i]
    if cls is Bxc:
        return Bxc()
    elif cls in [Adv, Bst, Out, Bdv, Cdv]:
        return cls(combos[j])
    else:
        return cls(literals[j])


def parse(lines):
    registers = []
    for line in lines:
        line = line.strip()
        if "Register" in line:
            registers.append(int(line.split(":")[1]))
        elif "Program" in line:
            instrs = [int(p) for p in line.split(":")[1].strip().split(",")]
            return registers, instrs


def part1(registers, instrs):
    prog = [parse_instr(i, j) for i, j in itertools.batched(instrs, 2)]
    print(prog)
    state = InterpreterState(0, registers, [])
    while state.ip < len(prog):
        prog[state.ip].apply(state)
    print(state.registers)
    return ",".join(str(v) for v in state.out)


def part2(_, instrs):
    def step(a, i):
        if i > len(instrs):
            return a
        printed = instrs[-i]
        for guess in range(8 * a, 8 * a + 8):
            b0 = guess % 8
            b1 = b0 ^ 3
            c = guess >> b1
            would_print = (b1 ^ c ^ 5) % 8
            if would_print == printed:
                print(f"{guess=} works")
                if aa := step(guess, i + 1):
                    return aa
        return None

    return step(0, 1)


if __name__ == "__main__":
    print(part1(*parse(sys.stdin)))
