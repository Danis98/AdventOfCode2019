edges = [x.split(")") for x in open("day06.input", "r").read().strip().split()]

tree = dict([(e, []) for x in edges for e in x])
conn_tot = 0

def create_tree():
    for edge in edges:
        tree[edge[0]].append(edge[1])

def get_sum(n):
    global conn_tot
    ctr = sum(map(lambda ch: get_sum(ch) + 1, tree[n]))
    conn_tot += ctr
    return ctr

create_tree()
get_sum("COM")
print(conn_tot)
