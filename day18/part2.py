lines = open("day18.input", "r").read().strip().split("\n")
grid = dict([((r, c), lines[r][c]) for r in range(len(lines)) for c in range(len(lines[r]))])

dir = {
    0: [-1, 0],
    1: [0, 1],
    2: [1, 0],
    3: [0, -1]
}

q = set()
d = {0: {}}

max_key_bitmap = 0
points = []
s = None
ch2pos = {}
for p in grid:
    if grid[p] not in '.#':
        if grid[p] == '@':
            s = p
        else:
            if grid[p] >= 'a' and grid[p] <= 'z':
                points.append(p)
                ch2pos[grid[p]] = p
                max_key_bitmap |= 1 << (ord(grid[p]) - ord('a'))
grid[(s[0]-1, s[1]-1)], grid[(s[0]-1, s[1])], grid[(s[0]-1, s[1]+1)] = '@', '#', '@'
grid[(s[0], s[1]-1)], grid[(s[0], s[1])], grid[(s[0], s[1]+1)] = '#', '#', '#'
grid[(s[0]+1, s[1]-1)], grid[(s[0]+1, s[1])], grid[(s[0]+1, s[1]+1)] = '@', '#', '@'
q.add((0, 0, ((s[0]-1, s[1]-1), (s[0]-1, s[1]+1), (s[0]+1, s[1]-1), (s[0]+1, s[1]+1)), "@"))

points += [(s[0]-1, s[1]-1), (s[0]-1, s[1]+1), (s[0]+1, s[1]-1), (s[0]+1, s[1]+1)]

def get_dist(n, par, reqs, target):
    if grid[n] >= 'A' and grid[n] <= 'Z':
        reqs |= 1 << (ord(grid[n]) - ord('A'))
    if n == target:
        return (0, reqs)
    if grid[n] >= 'a' and grid[n] <= 'z':
        reqs |= 1 << (ord(grid[n]) - ord('a'))
    for i in range(4):
        nxt = (n[0]+dir[i][0], n[1]+dir[i][1])
        if grid[nxt] == '#':
            continue
        if nxt == par:
            continue
        d = get_dist(nxt, n, reqs, target)
        if d is not None:
            return (d[0]+1, d[1])
    return None

point_dist = {}

for p1 in points:
    for p2 in points:
        point_dist[(p1, p2)] = get_dist(p1, (-1, -1), 0, p2)

def construct_quadrant(quadrant, start):
    queue = [(start, (-1, -1), [start])]
    while len(queue) > 0:
        n, p, r = queue.pop(0)
        r = list(r)
        if grid[n] >= 'a' and grid[n] <= 'z':
            if n not in quadrant:
                quadrant[n] = []
            for e in r:
                if e not in quadrant:
                    quadrant[e] = []
                quadrant[e].append(n)
            r.append(n)
        for i in range(4):
            nxt = (n[0]+dir[i][0], n[1]+dir[i][1])
            if grid[nxt] == '#' or nxt == p:
                continue
            queue.append((nxt, n, r))
    return quadrant

quadrant = {}
for i in range(4):
    p = min(q)[2][i]
    quadrant[i] = construct_quadrant({}, p)

while len(q) > 0:
    node = min(q)
    q.remove(node)
    steps, keys, pos, vis = node
    pos = list(pos)
    if keys & max_key_bitmap == max_key_bitmap:
        print(steps)
        break
    for robot in range(4):
        orig_pos = pos[robot]
        for next_point in quadrant[robot]:
            sym = grid[next_point]
            dist, req = point_dist[(orig_pos, next_point)]
            if sym in vis or req & keys != req:
                continue
            pos[robot] = next_point
            new_keys = keys
            if sym >= 'a' and sym <= 'z':
                new_keys |= 1 << (ord(sym)-ord('a'))
            if sym >= 'A' and sym <= 'Z':
                new_keys |= 1 << (ord(sym)-ord('A') + 26)
            nxt_tuple = (steps+dist, new_keys, tuple(pos), "".join(sorted(vis+sym)))
            if nxt_tuple in q:
                continue
            q.add(nxt_tuple)
        pos[robot] = orig_pos
