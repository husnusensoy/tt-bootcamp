from typing import Any, Tuple

lst = list(range(101))


name_surname = [
    ("husnu", "sensoy"),
    ("anil", "halil"),
    ("askar", "bozcan"),
    ("ersin", "fidan"),
    ("emre", "yahşi"),
]


def fn_surname(t: Tuple[str, str]) -> Any:
    _, surname = t

    return surname


# print(scoring)


def test_max():
    assert max(lst) == 100
    assert max(name_surname) == ("husnu", "sensoy")
    assert max(name_surname, key=fn_surname) == ("emre", "yahşi")
    assert min(name_surname, key=fn_surname) == ("askar", "bozcan")


print(sorted(name_surname, key=fn_surname))
