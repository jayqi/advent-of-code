from enum import Enum
from pathlib import Path
from string import ascii_lowercase
from typing import Optional

from pydantic import BaseModel, validator, ValidationError


PUZZLE_DIR = Path(__file__).parent


def read_file(file_name: str):
    with (PUZZLE_DIR / file_name).open("r") as fp:
        record = {}
        for line in fp:
            if line.strip():
                data = line.strip().split(" ")
                record.update(field.split(":") for field in data)
            else:
                yield record
                record = {}
        yield record


def is_valid(record: dict):
    required_fields = {
        "byr",
        "iyr",
        "eyr",
        "hgt",
        "hcl",
        "ecl",
        "pid",
    }
    return len(required_fields.difference(record.keys())) == 0


def part_one(file_name: str):
    records = read_file(file_name)
    valid = sum(is_valid(rec) for rec in records)
    print(f"{file_name} : {valid}")


class EyeColor(Enum):
    amb = "amb"
    blu = "blu"
    brn = "brn"
    gry = "gry"
    grn = "grn"
    hzl = "hzl"
    oth = "oth"


class Passport(BaseModel):
    byr: int
    iyr: int
    eyr: int
    hgt: str
    hcl: str
    ecl: EyeColor
    pid: str
    cid: Optional[str]

    @validator("byr")
    def birth_year(cls, v):
        assert 1920 <= v <= 2002
        return v

    @validator("iyr")
    def issue_year(cls, v):
        assert 2010 <= v <= 2020
        return v

    @validator("eyr")
    def expiration_year(cls, v):
        assert 2020 <= v <= 2030

    @validator("hgt")
    def height(cls, v):
        if v.endswith("cm"):
            val, _, _ = v.partition("cm")
            assert 150 <= int(val) <= 193
        elif v.endswith("in"):
            val, _, _ = v.partition("in")
            assert 59 <= int(val) <= 76
        else:
            raise ValueError
        return v

    @validator("hcl")
    def hair_color(cls, v):
        assert len(v) == 7
        assert v[0] == "#"
        valid_hex_chars = set(str(d) for d in range(10)) | set(ascii_lowercase[:6])
        assert not set(v[1:]).difference(valid_hex_chars)
        return v

    @validator("pid")
    def passport_id(cls, v):
        _ = int(v)
        assert len(v) == 9
        return v


def part_two(file_name: str):
    counter = 0
    for record in read_file(file_name):
        try:
            _ = Passport.parse_obj(record)
            counter += 1
        except ValidationError:
            pass
    print(f"{file_name} : {counter}")


if __name__ == "__main__":
    part_one("sample.txt")
    part_one("input.txt")
    print("---")
    part_two("sample.txt")
    part_two("sample2.txt")
    part_two("input.txt")
