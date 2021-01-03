from collections import Counter
from dataclasses import dataclass
from pathlib import Path


PUZZLE_DIR = Path(__file__).parent


@dataclass
class Policy:
    char: str
    rep_min: int
    rep_max: int

    @classmethod
    def from_text(cls, text: str):
        rep_range, _, char = text.partition(" ")
        rep_min, _, rep_max = rep_range.partition("-")
        return cls(char=char, rep_min=int(rep_min), rep_max=int(rep_max))

    def validate(self, password: str) -> bool:
        counter = Counter(password)
        return self.rep_min <= counter[self.char] <= self.rep_max

    def validate2(self, password: str) -> bool:
        pos1 = password[self.rep_min - 1]
        pos2 = password[self.rep_max - 1]
        return (self.char == pos1) != (self.char == pos2)  # one True, other False


@dataclass
class Password:
    policy: Policy
    password: str

    @classmethod
    def from_line(cls, line: str):
        policy, _, password = line.partition(": ")
        return cls(policy=Policy.from_text(policy), password=password)

    def is_valid(self):
        return self.policy.validate(self.password)

    def is_valid2(self):
        return self.policy.validate2(self.password)


def read_database(file_name: str):
    input_file = PUZZLE_DIR / file_name

    with input_file.open("r") as fp:
        return [Password.from_line(line) for line in fp]


def part_one(file_name: str):
    passwords = read_database(file_name)
    print(f"{file_name} : {sum(pwd.is_valid() for pwd in passwords)}")


def part_two(file_name: str):
    passwords = read_database(file_name)
    print(f"{file_name} : {sum(pwd.is_valid2() for pwd in passwords)}")


if __name__ == "__main__":
    part_one("sample.txt")
    part_one("input.txt")
    print("---")
    part_two("sample.txt")
    part_two("input.txt")
