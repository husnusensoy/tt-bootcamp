import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import List

import click
from click import argument, command, option
from faker import Faker
from tqdm import trange


@dataclass
class Profile:
    job: str
    company: str
    ssn: int
    blood_group: str
    username: str
    sex: str
    mail: str
    name: str
    website: List[str]


def get_next_profile(fake: Faker) -> Profile:
    prof = Profile(
        **fake.profile(
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
        )
    )

    return prof


@command()
@argument("file", nargs=1, type=click.Path(path_type=Path))
@option("--sample", default=10_000, help="Number of samples to generate")
def generate(file: Path, sample: int):
    fake = Faker("tr_TR")

    with file.open("w") as wp:
        for _ in trange(sample):
            p = get_next_profile(fake)

            print(json.dumps(asdict(p)), file=wp)


if __name__ == "__main__":
    generate()
