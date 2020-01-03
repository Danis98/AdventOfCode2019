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
                    is_outer = r + 1 >= len(lines)
                    portals[portal_id].append((-1 if is_outer else 1, (r-2, c)))
                else:
                    is_outer = r - 2 < 0
                    portals[portal_id].append((-1 if is_outer else 1, (r+1, c)))
            elif (r, c-1) in grid and grid[(r, c-1)] >= 'A' and grid[(r, c-1)] <= 'Z':
                portal_id = grid[(r, c-1)] + ch
                if portal_id not in portals:
                    portals[portal_id] = []
                if (r, c-2) in grid and grid[(r, c-2)] == '.':
                    is_outer = c + 1 >= len(lines[r])
                    portals[portal_id].append((-1 if is_outer else 1, (r, c-2)))
                else:
                    is_outer = c - 2 < 0
                    portals[portal_id].append((-1 if is_outer else 1, (r, c+1)))
        c += 1
    r += 1

start, end = None, None
for portal_id in portals:
    if portal_id == 'AA':
        start = (0, portals[portal_id][0][1])
    elif portal_id == 'ZZ':
        end = (0, portals[portal_id][0][1])
    else:
        p_a, p_b = portals[portal_id]
        warps[p_a[1]] = (p_a[0], p_b[1])
        warps[p_b[1]] = (p_b[0], p_a[1])

dir = {
    0: [-1, 0],
    1: [0, 1],
    2: [1, 0],
    3: [0, -1]
}

q = [start]
dist = {start: 0}
par = {start: None}
while len(q) > 0:
    n = q.pop(0)
    if n == end:
        break
    for d in dir:
        nxt = (n[0], (n[1][0]+dir[d][0], n[1][1]+dir[d][1]))
        if nxt[1] not in grid or grid[nxt[1]] != '.' or nxt in dist:
            continue
        dist[nxt] = dist[n] + 1
        par[nxt] = n
        q.append(nxt)
    if n[1] in warps:
        nxt = (n[0] + warps[n[1]][0], warps[n[1]][1])
        if nxt in dist or nxt[0] < 0:
            continue
        dist[nxt] = dist[n] + 1
        par[nxt] = n
        q.append(nxt)
print(dist[end])
