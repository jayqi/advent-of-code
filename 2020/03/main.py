from dataclasses import dataclass
from math import prod
from pathlib import Path
from typing import List

PUZZLE_DIR = Path(__file__).parent


@dataclass
class Line:
    text: str

    def is_tree(self, pos: int):
        mod_pos = pos % len(self.text)
        return self.text[mod_pos] == "#"


@dataclass
class Map:
    lines: List[Line]

    @classmethod
    def from_file(cls, path: Path):
        with path.open("r") as fp:
            return cls(lines=[Line(text=line.strip()) for line in fp])

    def count_trees(self, run: int, fall: int):
        counter = 0
        for loop_ind, line_ind in enumerate(range(len(self.lines))[::fall]):
            pos = loop_ind * run
            counter += self.lines[line_ind].is_tree(pos)
        return counter


def solve(file_name: str, run, fall):
    map = Map.from_file(path=PUZZLE_DIR / file_name)
    trees = map.count_trees(run=run, fall=fall)
    print(f"{file_name}, run={run}, fall={fall} : {trees}")
    return trees


if __name__ == "__main__":
    print("# Part One")
    solve("sample.txt", 3, 1)
    solve("input.txt", 3, 1)
    print("---")
    print("# Part Two")
    slopes = [
        (1, 1),
        (3, 1),
        (5, 1),
        (7, 1),
        (1, 2),
    ]
    for file_name in ["sample.txt", "input.txt"]:
        counts = [solve(file_name, run=run, fall=fall) for run, fall in slopes]
        print(f"{' * '.join(map(str, counts))} = {prod(counts)}")
