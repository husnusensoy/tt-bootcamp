import json
from pprint import pprint

profiles = []
with open("data/profiles.jsonl") as fp:
    for i, line in enumerate(fp):
        d = json.loads(line)

        profiles.append(d)

        if i == 4:
            break

pprint(profiles)
