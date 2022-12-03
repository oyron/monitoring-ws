import sys

def priority(item):
    return (ord(item) - 96) if ord(item) > 90 else (ord(item) - 64 + 26)

data = [line.strip() for line in sys.stdin.readlines()]

rucksacks = [[item[0:int(len(item) / 2)], item[int(len(item)/2):]] for item in data]
in_both = [list(set(rucksack[0]) & set(rucksack[1]))[0] for rucksack in rucksacks]
print(sum([priority(item) for item in in_both]))

triples = [data[i-2:i+1] for i in range(len(data)) if (i+1) % 3 == 0]
in_all = [list(set(triple[0]) & set(triple[1]) & set(triple[2]))[0] for triple in triples]
print(sum([priority(val) for val in in_all]))
