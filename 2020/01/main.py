from pathlib import Path

PUZZLE_DIR = Path(__file__).parent


def read_expenses():
    input_file = PUZZLE_DIR / "input.txt"

    with input_file.open("r") as fp:
        return [int(line) for line in fp]


def part_one():
    expenses = read_expenses()

    # expense: (2020-expense)
    expense_map = {exp: (2020 - exp) for exp in expenses if exp <= 2020}

    for key, value in expense_map.items():
        if value in expense_map:
            print(f"{key} * {value} = {key*value}")
            break


def part_two():
    expenses = read_expenses()

    # (2020-expense): expense
    reverse_expense_map = {(2020 - exp): exp for exp in expenses if exp <= 2020}

    for exp1 in reverse_expense_map.values():
        for exp2 in reverse_expense_map.values():
            if (exp1 + exp2) in reverse_expense_map:
                exp3 = reverse_expense_map[exp1 + exp2]
                print(f"{exp1} * {exp2} * {exp3} = {exp1*exp2*exp3}")
                return


if __name__ == "__main__":
    part_one()
    print("---")
    part_two()
