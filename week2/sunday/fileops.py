from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Tuple

from pprint import pprint
import json


@dataclass
class Employee:
    name: str
    surname: str
    age: int
    company: str
    city: str
    is_admin: bool = False


def write_employees(
    employee_list: List[Employee], file_name: str, format: str = "jsonl", **kwargs
):
    def write_delimited_file(
        lod: List[dict], target: Path, columns: List[str], delimiter: str = '|'
    ) -> Tuple[int, int]:
        nbytes, nlines = 0, 0

        with target.open("w") as wp:
            for d in lod:
                line = delimiter.join([d[c] for c in columns])

                nbytes += len(line)
                nlines += 1
                print(line, file=wp)

        return nbytes, nlines

    def write_json_file(lod: List[dict], target: Path) -> Tuple[int, int]:
        nbytes, nlines = 0, 0

        with target.open("w") as wp:
            for d in lod:
                line = json.dumps(d)

                nbytes += len(line)
                nlines += 1
                print(line, file=wp)

        return nbytes, nlines

    if format == "jsonl":
        nbytes, nlines = write_json_file(
            [asdict(e) for e in employee_list], Path(file_name)
        )
    else:
        nbytes, nlines = write_delimited_file(
            [asdict(e) for e in employee_list],
            Path(file_name),
            delimiter=kwargs['delimiter'],
            columns=kwargs['columns'],
        )

    print(f"Write operation generated {nlines} lines of {nbytes} bytes")


def read_employees(
    file_name: str | Path, header: bool, delimiter: str = ","
) -> List[Employee]:
    if isinstance(file_name, Path):
        file_ob = file_name
    else:
        file_ob = Path(file_name)

    resultset: List[Employee] = []

    with file_ob.open() as fp:
        if header:
            for i, line in enumerate(fp):
                if i == 0:
                    # header
                    headers = [h.lower() for h in line.strip().split(delimiter)]
                else:
                    fullname, age_s, company, city = line.strip().split(delimiter)

                    *rest, surname = fullname.split()

                    e = Employee(
                        name=" ".join(rest),
                        surname=surname,
                        age=int(age_s),
                        company=company,
                        city=city,
                    )

                    resultset.append(e)
        else:
            for i, line in enumerate(fp):
                fullname, age_s, company, city = line.strip().split(delimiter)

                *rest, surname = fullname.split()

                e = Employee(
                    name=" ".join(rest),
                    surname=surname,
                    age=int(age_s),
                    company=company,
                    city=city,
                )

                resultset.append(e)

    return resultset


def test_employee():
    assert len(read_employees("data/sample.csv", header=True)) == 4
    assert len(read_employees(Path("data/sample.csv"), header=True)) == 4


if __name__ == "__main__":
    employees = read_employees("data/sample.csv", header=True)

    print(employees)

    write_employees(employees, "data/sample.jsonl")
    
    write_employees(employees, "data/sample.txt", "delimiter", columns=["city","name"], delimiter="|")
