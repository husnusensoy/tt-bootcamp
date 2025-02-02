from pprint import pprint
import re

raw_data = {
    "name": ["Husnu Sensoy", "İnanç Dokurel", "Kerem Kargın"],
    "company": ["Global Maksimum"] * 3,
    "age": ["42", "31", "28"],
}


RE_INTEGER = re.compile(r"-?\d+")


def is_integer(s: str) -> bool:
    try:
        _ = int(s)

        return True
    except:
        return False


def is_integer_2(s: str) -> bool:
    if s.startswith("-"):
        return all([c in "0123456789" for c in s[1:]])
    else:
        return all([c in "0123456789" for c in s])


def is_integer_3(s: str) -> bool:
    return RE_INTEGER.match(s) is not None


if __name__ == "__main__":
    processed_data = {}
    for k in raw_data:
        if all([is_integer(e) for e in raw_data[k]]):
            processed_data[k] = [int(e) for e in raw_data[k]]
        else:
            processed_data[k] = [e for e in raw_data[k]]

    pprint(processed_data)
