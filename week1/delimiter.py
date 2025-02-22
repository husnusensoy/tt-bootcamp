import json
from pathlib import Path

import click
from click import argument, command, option
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

sizes = [44, 35, 35, 11, 3, 21, 1, 33, 4]
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
@argument("csv", nargs=1, type=click.Path(path_type=Path))
@option("--delimiter", default=",", help="Delimiter")
def analyze(jsonl: Path, csv: Path, delimiter: str):
    with jsonl.open("r") as rp, csv.open("w") as wp:
        for profile in [json.loads(p) for p in tqdm(rp)]:
            line = delimiter.join([profile[field] for field in fields if field not in ["website"]])

            print(line, file=wp)


if __name__ == "__main__":
    analyze()
