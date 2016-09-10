import sys
import requests
from collections import defaultdict, deque

url="https://www.wikidata.org/w/api.php?action=wbgetentities&ids={}&format=json"
sister_city = "P190"

seen = set()
names, relations = {}, defaultdict(list)
agenda = deque()

with open("agenda") as f:
    agenda.extend(l.strip() for l in f)
    print("Loaded agenda with size", len(agenda), file=sys.stdout)

with open("names.tsv") as f:
    for line in f:
        ID, name = line.strip().split("\t")
        names[ID] = name
        seen.add(ID)
    print("Loaded names with size", len(names), file=sys.stdout)

pref_langs = ['de', 'en', 'fr', 'it', 'es']


def get_name(d, pref_langs):
    for lang in pref_langs:
        if d.get(lang, False):
            return d[lang]["value"]
    return None

try:
    input("Start crawling? [Y]")
    while agenda:
        next_ones = filter(lambda x: x not in seen, [agenda.popleft() for _ in range(10) if agenda])
        r = requests.get(url.format("|".join(next_ones)))
        j = r.json()
        if j["success"] != 1:
            continue
        if not j.get("entities", False):
            continue
        for current_city in j["entities"]:
            name = get_name(j["entities"][current_city]["labels"], pref_langs)
            if name:
                names[current_city] = name
            sisters = j["entities"][current_city]["claims"].get(sister_city, [])
            for sis in sisters:
                try:
                    sis_id = sis["mainsnak"]["datavalue"]["value"]["id"]
                    relations[current_city].append(sis_id)
                    agenda.append(sis_id)
                    print("{} is partnered with {}".format(names.get(current_city, "ID " + current_city), names.get(sis_id, "ID " + sis_id)), file=sys.stderr)
                except:
                    pass
            seen.add(current_city)
finally:
    with open("names.tsv", "w") as f:
        for ID in names:
            print(ID, names[ID], sep="\t", file=f)

    with open("relations.tsv", "a") as f:
        for ID in relations:
            for sis_id in relations[ID]:
                print(ID, sis_id, sep="\t", file=f)

    with open("agenda", "w") as f:
        for item in agenda:
            f.write(item + "\n")
