import sys
from collections import defaultdict

def parse_program(infile):
    for line in infile:
        operation, argument = line.strip().split()
        yield operation, int(argument)


def flip_instructions(program):
    return map(flip_instruction, program)


def flip_instruction(instruction):
    operation, argument = instruction

    if operation == "jmp":
        operation = "nop"
    elif operation == "nop":
        operation = "jmp"

    return operation, argument


def get_steps(program):
    for index, (operation, argument) in enumerate(program):
        if operation == "jmp":
            yield (index, index + argument)
        else:
            yield (index, index + 1)


def build_moves(steps):
    moves = defaultdict(list)
    for src, dst in steps:
        moves[src].append(dst)
    return moves        


def reachable(moves, start):
    to_visit = [start]
    visited = set()

    while to_visit:
        current = to_visit.pop()
        if current in visited:
            continue

        visited.add(current)
        to_visit.extend(moves[current])

    return visited


def instruction_to_flip(program):
    steps = list(get_steps(program))

    forwards = build_moves(steps)
    reachable_forwards = reachable(forwards, 0)

    backwards = build_moves((dst, src) for (src, dst) in steps)
    reachable_backwards = reachable(backwards, len(program))

    alternate = flip_instructions(program)
    alternate_steps = dict(get_steps(alternate))

    return next(index for index in reachable_forwards if alternate_steps[index] in reachable_backwards)


def run(program):
    pc = 0
    acc = 0

    while pc < len(program):
        operation, argument = program[pc]

        if operation == "acc":
            acc += argument
            pc += 1
        elif operation == "nop":
            pc += 1
        elif operation == "jmp":
            pc += argument
        else:
            raise Exception(f"Unknown operation '{operation}'")

    return acc


def main():
    program = list(parse_program(sys.stdin))

    to_flip = instruction_to_flip(program)

    program[to_flip] = flip_instruction(program[to_flip])

    print(run(program))


if __name__ == "__main__":
    main()    