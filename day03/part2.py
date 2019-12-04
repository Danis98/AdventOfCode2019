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
    dist = 0
    for move in w:
        d = dir[move[0]]
        l = int(move[1:])
        for i in range(l):
            pos = (pos[0]+d[0], pos[1]+d[1])
            dist += 1
            if pos in grid and grid[pos][id] == 0:
                grid[pos][id] = dist
            else:
                grid[pos] = [0, 0]
                grid[pos][id] = dist

write_wire(wA, 0)
write_wire(wB, 1)

print(min([sum(grid[p]) for p in grid if grid[p][0] != 0 and grid[p][1] != 0]))
