import math

lines = open("day14.input", "r").read().strip().split("\n")

craft_tree = {"ORE": (1, [])}
needed_parts = {}

for line in lines:
    reag, res = [h.split(", ") for h in line.split(" => ")]
    reag = list(map(lambda r: (int(r.split(" ")[0]), r.split(" ")[1]), reag))
    res = (int(res[0].split(" ")[0]), res[0].split(" ")[1])
    craft_tree[res[1]] = (res[0], reag)

sort_seq = []
vis = set()
def toposort(n, p):
    if n in vis:
        return
    vis.add(n)
    for el in craft_tree[n][1]:
        toposort(el[1], n)
    sort_seq.insert(0, n)
toposort("FUEL", "")

def count_needed(start):
    for n in sort_seq:
        q = needed_parts[n]
        unit = craft_tree[n][0]
        recipe = craft_tree[n][1]
        mult = math.ceil(float(q)/unit)
        needed_parts[n] = mult * unit
        cnt = 0
        for element in recipe:
            if element[1] not in needed_parts:
                needed_parts[element[1]] = 0
            needed_parts[element[1]] += mult * element[0]

one_trln = 1000000000000
a = 1
b = one_trln
while a < b:
    mid = (a+b+1)//2
    needed_parts = {"FUEL": mid}
    count_needed("FUEL")
    if needed_parts["ORE"] > one_trln:
        b = mid - 1
    else:
        a = mid
print(a)
