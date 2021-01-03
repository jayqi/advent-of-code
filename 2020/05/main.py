from pathlib import Path


PUZZLE_DIR = Path(__file__).parent


def read_file(file_name: str):
    with (PUZZLE_DIR / file_name).open("r") as fp:
        return [
            (
                int(line[0:7].replace("F", "0").replace("B", "1"), 2),
                int(line[7:10].replace("L", "0").replace("R", "1"), 2),
            )
            for line in fp
        ]


def part_one(file_name):
    seats = read_file(file_name)
    max_id = max(row * 8 + col for row, col in seats)
    print(f"{file_name} : {max_id}")


def part_two(file_name):
    seat_ids = sorted(row * 8 + col for row, col in read_file(file_name))
    print(seat_ids)
    for ind, val in enumerate(seat_ids):
        if seat_ids[ind + 1] != (val + 1):
            print(f"{file_name} : {val+1}")
            break


if __name__ == "__main__":
    part_one("sample.txt")
    part_one("input.txt")
    print("---")
    part_two("input.txt")
