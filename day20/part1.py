lines = open("day20.input", "r").read().strip("\n").split("\n")

grid = {}
portals = {}
warps = {}

r, c = 0, 0
for line in lines:
    c = 0
    for ch in line:
        grid[(r, c)] = ch
        if ch >= 'A' and ch <= 'Z':
            portal_id = ""
            if (r-1, c) in grid and grid[(r-1, c)] >= 'A' and grid[(r-1, c)] <= 'Z':
                portal_id = grid[(r-1, c)] + ch
                if portal_id not in portals:
                    portals[portal_id] = []
                if (r-2, c) in grid and grid[(r-2, c)] == '.':
                    portals[portal_id].append((r-2, c))
                else:
                    portals[portal_id].append((r+1, c))
            elif (r, c-1) in grid and grid[(r, c-1)] >= 'A' and grid[(r, c-1)] <= 'Z':
                portal_id = grid[(r, c-1)] + ch
                if portal_id not in portals:
                    portals[portal_id] = []
                if (r, c-2) in grid and grid[(r, c-2)] == '.':
                    portals[portal_id].append((r, c-2))
                else:
                    portals[portal_id].append((r, c+1))
        c += 1
    r += 1

start, end = None, None
for portal_id in portals:
    if portal_id == 'AA':
        start = portals[portal_id][0]
    elif portal_id == 'ZZ':
        end = portals[portal_id][0]
    else:
        p_a, p_b = portals[portal_id]
        warps[p_a] = p_b
        warps[p_b] = p_a

dir = {
    0: [-1, 0],
    1: [0, 1],
    2: [1, 0],
    3: [0, -1]
}

q = [start]
dist = {start: 0}
while len(q) > 0:
    n = q.pop(0)
    if n == end:
        break
    for d in dir:
        nxt = (n[0]+dir[d][0], n[1]+dir[d][1])
        if nxt not in grid or grid[nxt] != '.' or nxt in dist:
            continue
        dist[nxt] = dist[n] + 1
        q.append(nxt)
    if n in warps and warps[n] not in dist:
        dist[warps[n]] = dist[n] + 1
        q.append(warps[n])

print(dist[end])
