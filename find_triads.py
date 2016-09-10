import sys
from collections import defaultdict

names, relations = {}, defaultdict(set)

with open("names.tsv") as f:
    for line in f:
        ID, name = line.strip().split("\t")
        names[ID] = name
    print("Loaded names with size", len(names), file=sys.stdout)

name2id = {name: ID for ID, name in names.items()}

with open("relations.tsv") as f:
    for line in f:
        a, b = line.strip().split("\t")
        relations[a].add(b)
        relations[b].add(a)
    print("Loaded relations with size", len(relations), file=sys.stdout)

def n(ID):
    return names.get(ID, "ID " + ID)

print("Finding triads...", file=sys.stdout)
# print("Karkkila:", ", ".join(n(i) for i in relations[name2id["Karkkila"]]))
# print("Niederanven:", ", ".join(n(i) for i in relations[name2id["Niederanven"]]))
# print("Zvolen:", ", ".join(n(i) for i in relations[name2id["Zvolen"]]))
# sys.exit()
for start in relations:
    for middle in relations[start]:
        for end in relations[middle]:
            if end in relations[start]:
                print("Triad found: {} {} {}".format(n(start), n(middle), n(end)))
