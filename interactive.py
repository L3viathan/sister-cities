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

current = ""
ID = ""
sisters = []
try:
    while True:
        i = input(current + "> ")
        if i in "?h":
            print(
                    """    g Townname       Go to Townname
    s                Show sister towns
    f query          Find towns containing query
    i                Show ID"""
                       )
        elif i == "s":
            sisters = list(relations[ID])
            print("\t" + "\n\t".join(str(nu+1) + ": " + n(s) for nu, s in zip(range(99), sisters)))
        elif i.startswith("f "):
            _, search = i.split(" ", 1)
            sisters = []
            nu = 0
            for town in names:
                if search.lower() in n(town).lower():
                    nu += 1
                    sisters.append(town)
                    print("\t{}: {}".format(nu, n(town)))
        elif i.startswith("g "):
            _, town = i.split(" ", 1)
            if town in name2id:
                ID = name2id[town]
                current = town
            elif town.isnumeric():
                num = int(town)
                if len(sisters) >= num:
                    ID = sisters[num-1]
                    current = n(ID)
        elif i == "i":
            print("{}: ID {}".format(current, ID))
        else:
            print("Unknown command")
except KeyboardInterrupt:
    pass
except EOFError:
    pass
