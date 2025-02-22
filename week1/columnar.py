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
@argument("columnar", nargs=1, type=click.Path(path_type=Path))
@option("--delimiter", default=",", help="Delimiter")
def analyze(jsonl: Path, columnar: Path, delimiter: str):
    columnar.mkdir(exist_ok=True, parents=True)

    files = [(columnar / field).open("w") for field in fields]

    with jsonl.open("r") as rp:
        for profile in [json.loads(p) for p in tqdm(rp)]:
            for file, field in zip(files, fields):
                print(profile[field], file=file)


if __name__ == "__main__":
    analyze()
