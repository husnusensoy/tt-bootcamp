import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple, Union


@dataclass
class Profile:
    job: str
    company: str
    ssn: str
    blood_group: str
    username: str
    sex: str
    mail: str
    name: str
    website: List[str]


class ProfileDB:
    db: Dict[int, Dict[str, Union[str, List[str]]]]

    def __init__(self, db_file: Path = Path("../data/profiles.jsonl")):
        self.db_file = db_file

        print("Loading database...")

        with self.db_file.open() as fp:
            db = [json.loads(line) for line in fp]

        self.db = {int(d["ssn"]): d for d in db}

        print("Loaded")

    def get_profile_by_ssn(self, ssn: int) -> Profile:
        e: dict = self.db[ssn]
        # e = [d for d in self.db if int(d["ssn"]) == ssn][0]

        return Profile(**e)

    def count_profile_by_job(self, job: List[str]) -> int:
        return sum([1 for p in self.db.values() if p["job"] in job])

    def count_profile_by_field(self, field: Tuple[str]) -> Dict[Tuple, int]:
        result = {}

        for p in self.db.values():
            group = tuple([p[f] for f in field])

            result[group] = result.get(group, 0) + 1

        return result

    def listagg_profile_by_field(self, field: Tuple[str]) -> Dict[Tuple, List[int]]:  # noqa: E501
        result = {}

        for p in self.db.values():
            group = tuple([p[f] for f in field])

            if group not in result:
                result[group] = []

            result[group].append(int(p["ssn"]))

        return result

    def count_profile(self):
        return len(self.db)


def test_profile_by_ssn():
    db = ProfileDB()

    assert db.get_profile_by_ssn(93211946296) == Profile(
        job="İcra memuru",
        company="Netlog Lojistik Hizmetleri",
        ssn="93211946296",
        blood_group="B-",
        username="dkisakurek",
        sex="M",
        mail="tbilgin@outlook.com",
        name="Okt. Erik Kayagün Demirel",
        website=["https://www.basf.com/", "https://ocalan.net/"],
    )


def test_count_profile():
    db = ProfileDB()

    assert db.count_profile() == 100_000


def test_count_profile_by_job():
    db = ProfileDB()

    assert db.count_profile_by_job(["İnşaat mühendisi", "İnşaatçı"]) == 272


def test_count_profile_by_field():
    db = ProfileDB()

    assert (
        db.count_profile_by_field(("blood_group",)) is None
    )  # {("B-","M"): 10,("B-","F"): 10}


def test_listagg_profile_by_field():
    db = ProfileDB()

    assert (
        db.listagg_profile_by_field(("sex", "company")) is None
    )  # {("B-","M"): 10,("B-","F"): 10}


# def test_count_profile():
#     db = ProfileDB()
#     # Implemnt this by key get function
#     assert db.count_profile_by_field((,)) == [("B-","M", 10),("B-","F", 10)]
