import json
from pathlib import Path

import click
from click import argument, command
from tqdm import tqdm

"""
name            S44
job             S35
company         S35
ssn             I11
blood_group     S3
username        S21
sex             S1
mail            S33
website         S4
"""


sizes = [48, 35, 35, 11, 3, 22, 1, 35, 4]

fields = [
    "name",
    "job",
    "company",
    "ssn",
    "blood_group",
    "username",
    "sex",
    "mail",
    "website",
]


@command()
@argument("jsonl", nargs=1, type=click.Path(exists=True, path_type=Path))
@argument("fix-length", nargs=1, type=click.Path(path_type=Path))
def analyze(jsonl: Path, fix_length: Path):
    with jsonl.open("r") as rp, fix_length.open("w") as wp:
        for profile in [json.loads(p) for p in tqdm(rp)]:
            line = ""
            for field, size in zip(fields, sizes):
                if field == "website":
                    continue

                field = profile[field].ljust(size, " ")
                line += field

            print(line, file=wp)


if __name__ == "__main__":
    analyze()
