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
for p in grid:
    if grid[p] == '@':
        q.add((0, p, 0))
    elif grid[p] >= 'a' and grid[p] <= 'z':
        max_key_bitmap |= 1 << (ord(grid[p]) - ord('a'))

while len(q) > 0:
    n = min(q)
    q.remove(n)
    dst, pos, key_bitmap = n
    print(n, max_key_bitmap)
    if (pos, key_bitmap) not in d or d[(pos, key_bitmap)] < dst:
        d[key_bitmap][pos] = dst
    if key_bitmap == max_key_bitmap:
        print(dst)
        break
    for i in range(4):
        nxt = (pos[0]+dir[i][0], pos[1]+dir[i][1])
        nxt_key_bitmap = key_bitmap
        if grid[nxt] == '#':
            continue
        if grid[nxt] >= 'A' and grid[nxt] <= 'Z':
            if (key_bitmap >> (ord(grid[nxt]) - ord('A'))) % 2 == 0:
                continue
        if grid[nxt] >= 'a' and grid[nxt] <= 'z':
            nxt_key_bitmap |= 1 << (ord(grid[nxt]) - ord('a'))
        if nxt_key_bitmap not in d:
            d[nxt_key_bitmap] = {}
        if nxt in d[nxt_key_bitmap] and d[nxt_key_bitmap][nxt] < dst + 1:
            continue
        for k in d:
            if (k == nxt_key_bitmap or k > nxt_key_bitmap and k ^ nxt_key_bitmap != 0) \
                    and nxt in d[k] and d[k][nxt] < dst + 1:
                continue
        d[nxt_key_bitmap][nxt] = dst + 1
        q.add((dst+1, nxt, nxt_key_bitmap))
