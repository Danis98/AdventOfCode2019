wA, wB = [x.split(",") for x in open("day03.input", "r").read().strip().split()]

dir = {
    'U': [0, 1],
    'R': [1, 0],
    'D': [0, -1],
    'L': [-1, 0]
}

grid = {}

def write_wire(w, id):
    pos = (0, 0)
    for move in w:
        d = dir[move[0]]
        l = int(move[1:])
        for i in range(l):
            pos = (pos[0]+d[0], pos[1]+d[1])
            if pos in grid:
                grid[pos] |= id
            else:
                grid[pos] = id

write_wire(wA, 1)
write_wire(wB, 2)

print(min([abs(p[0])+abs(p[1]) for p in grid if grid[p] == 3]))
