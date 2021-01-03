from collections import Counter
from pathlib import Path
from typing import Tuple


PUZZLE_DIR = Path(__file__).parent


def read_file(file_name: str):
    with (PUZZLE_DIR / file_name).open("r") as fp:
        group = []
        for line in fp:
            if line.strip():
                group.append(line.strip())
            else:
                yield "".join(group)
                group = []
        yield "".join(group)


def part_one(file_name: str):
    counts = [Counter(group) for group in read_file(file_name)]
    score = sum(len(counter.keys()) for counter in counts)
    print(f"{file_name} : {score}")


def read_file2(file_name: str) -> Tuple[int, str]:
    """Output is (group_size, responses)"""
    with (PUZZLE_DIR / file_name).open("r") as fp:
        group = []
        for line in fp:
            if line.strip():
                group.append(line.strip())
            else:
                yield (len(group), "".join(group))
                group = []
        yield (len(group), "".join(group))


def part_two(file_name: str):
    counts = [(grp_size, Counter(grp_resp)) for grp_size, grp_resp in read_file2(file_name)]
    score = sum(
        sum(grp_size == resp_ct for resp_ct in grp_counter.values())
        for grp_size, grp_counter in counts
    )
    print(f"{file_name} : {score}")


if __name__ == "__main__":
    part_one("sample.txt")
    part_one("input.txt")
    print("---")
    part_two("sample.txt")
    part_two("input.txt")
