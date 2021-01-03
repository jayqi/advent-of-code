from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional

PUZZLE_DIR = Path(__file__).parent


@dataclass
class RuleSet:
    mapping: Dict[str, Dict[str, int]]

    @classmethod
    def from_file(cls, file_name: str):
        with (PUZZLE_DIR / file_name).open("r") as fp:
            mapping = dict(cls.parse_rule(line) for line in fp)
        return cls(mapping)

    @staticmethod
    def parse_rule(text: str):
        # light red bags contain 1 bright white bag, 2 muted yellow bags.
        outer, _, inner = text.partition(" contain ")

        # light red bags
        outer, _, _ = outer.partition(" bag")

        # 1 bright white bag, 2 muted yellow bags.
        content_texts = [
            content.strip() for content in inner.split(",") if "no other" not in content
        ]

        contents = {}
        for content_text in content_texts:
            # 2 muted yellow bags.
            num_text, _, bag_text = content_text.partition(" ")
            color, _, _ = bag_text.partition(" bag")
            contents.update({color: int(num_text)})

        return (outer, contents)

    def crawl_bag(self, color: str, track_visited: Optional[set] = None):
        """Pass empty set to track_visited to short-circuit visited colors, if we don't care about
        a full search.
        """

        yield color

        if track_visited is not None:
            track_visited.add(color)

        for inner_color in self.mapping[color].keys():

            if track_visited is not None:
                if inner_color in track_visited:
                    continue

            for _ in range(self.mapping[color][inner_color]):
                yield from self.crawl_bag(inner_color, track_visited=track_visited)

    def has_shiny_gold(self, color: str):
        for found in self.crawl_bag(color, track_visited=set()):
            if found == "shiny gold":
                return True
        return False


def part_one(file_name: str):
    ruleset = RuleSet.from_file(file_name)
    count = sum(
        ruleset.has_shiny_gold(color) for color in ruleset.mapping.keys() if color != "shiny gold"
    )
    print(f"{file_name} : {count}")


def part_two(file_name: str):
    ruleset = RuleSet.from_file(file_name)
    bags = sum(1 for _ in ruleset.crawl_bag("shiny gold")) - 1
    print(f"{file_name} : {bags}")


if __name__ == "__main__":
    part_one("sample.txt")
    part_one("input.txt")
    print("---")
    part_two("sample.txt")
    part_two("sample2.txt")
    part_two("input.txt")
