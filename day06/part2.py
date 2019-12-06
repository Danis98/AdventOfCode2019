edges = [x.split(")") for x in open("day06.input", "r").read().strip().split()]

tree = dict([(e, []) for x in edges for e in x])
conn_tot = 0

def create_tree():
    for edge in edges:
        tree[edge[0]].append(edge[1])
        tree[edge[1]].append(edge[0])

def get_dist(start, end):
    q = [start]
    d = {start: 0}
    while len(q) > 0:
        n = q.pop(0)
        for ch in tree[n]:
            if ch in d:
                continue
            d[ch] = d[n] + 1
            if ch == end:
                return d[ch]
            q.append(ch)
    return -1

create_tree()
print(get_dist('YOU', 'SAN') - 2)
