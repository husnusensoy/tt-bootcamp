from pprint import pprint

sizes = [48, 35, 35, 11, 3, 22, 1, 35]
begins = [0, 48, 83, 118, 129, 132, 154, 155]
ends = [48, 83, 118, 129, 132, 154, 155, 190]

fields = ["name", "job", "company", "ssn", "blood_group", "username", "sex", "mail"]

profiles = []
with open("data/profiles.txt") as fp:
    for i, line in enumerate(fp):
        d = {}
        for field, ibegin, iend in zip(fields, begins, ends):
            d[field] = line[ibegin:iend].rstrip()

        profiles.append(d)

        if i == 4:
            break

pprint(profiles)
