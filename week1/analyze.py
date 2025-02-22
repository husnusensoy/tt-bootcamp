import json
from pathlib import Path

import click
from click import argument, command
from tqdm import tqdm


@command()
@argument("file", nargs=1, type=click.Path(exists=True, path_type=Path))
def analyze(file: Path):
    with file.open("r") as wp:
        profiles = [json.loads(p) for p in tqdm(wp)]

    for field in tqdm(
        [
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
    ):
        if field == "ssn":
            mx = len(str(max([p[field] for p in profiles])))

            print(f"{field:<15} I{mx}")
        else:
            mx = len(max([p[field] for p in profiles], key=lambda x: len(x)))
            print(f"{field:<15} S{mx}")


if __name__ == "__main__":
    analyze()
