from pathlib import Path
from typing import List, Tuple


PUZZLE_DIR = Path(__file__).parent


def acc(value: int, accumulator: int, instr_ind: int) -> (int, int):
    accumulator += value
    next_instr_ind = instr_ind + 1
    return (accumulator, next_instr_ind)


def jmp(value: int, accumulator: int, instr_ind: int) -> (int, int):
    next_instr_ind = instr_ind + value
    return (accumulator, next_instr_ind)


def nop(value: int, accumulator: int, instr_ind: int) -> (int, int):
    next_instr_ind = instr_ind + 1
    return (accumulator, next_instr_ind)


dispatcher = {
    "acc": acc,
    "jmp": jmp,
    "nop": nop,
}


def execute(instructions: List[Tuple[str, int]]):
    ind = 0
    accumulator = 0
    executed = set()
    while ind not in executed:
        executed.add(ind)
        try:
            op, val = instructions[ind]
        except IndexError:
            return (True, accumulator)
        accumulator, ind = dispatcher[op](value=val, accumulator=accumulator, instr_ind=ind)
    return (False, accumulator)


def read_file(file_name: str):
    with (PUZZLE_DIR / file_name).open("r") as fp:
        for line in fp:
            op, _, val = line.partition(" ")
            yield (op, int(val))


def part_one(file_name: str):
    instructions = list(read_file(file_name))
    succeeded, accumulator = execute(instructions)
    print(f"{file_name} : {accumulator}")


def part_two(file_name: str):
    instructions = list(read_file(file_name))
    for ind, instr in enumerate(instructions):
        if instr[0] == "acc":
            continue

        new_instructions = instructions.copy()
        if instr[0] == "nop":
            new_instructions[ind] = ("jmp", new_instructions[ind][1])
        elif instr[0] == "jmp":
            new_instructions[ind] = ("nop", new_instructions[ind][1])

        succeeded, accumulator = execute(new_instructions)
        if succeeded:
            print(f"{file_name} : {accumulator}")
            break


if __name__ == "__main__":
    part_one("sample.txt")
    part_one("input.txt")
    print("---")
    part_two("sample.txt")
    part_two("input.txt")
