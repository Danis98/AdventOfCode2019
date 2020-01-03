grids = {}
grids[0] = list(map(list, open("day24.input", "r").read().split()))
grids[1] = [['.' for j in range(5)] for i in range(5)]
grids[-1] = [['.' for j in range(5)] for i in range(5)]

def do_step(grids):
    new_grids = {}
    for level in grids:
        if '#' in "".join(["".join(grids[level][r]) for r in range(5)]):
            if level - 1 not in grids:
                new_grids[level - 1] = [['.' for j in range(5)] for i in range(5)]
            if level + 1 not in grids:
                new_grids[level + 1] = [['.' for j in range(5)] for i in range(5)]
        new_grid = []
        for i in range(5):
            row = []
            for j in range(5):
                if (i, j) == (2, 2):
                    row.append('?')
                    continue
                neigh = 0
                if (i, j) == (3, 2) and level + 1 in grids:
                    neigh += (grids[level+1][4][0] == '#') + \
                                (grids[level+1][4][1] == '#') + \
                                (grids[level+1][4][2] == '#') + \
                                (grids[level+1][4][3] == '#') + \
                                (grids[level+1][4][4] == '#')
                else:
                    neigh += grids[level][i-1][j] == '#' if i>0 else level - 1 in grids and grids[level-1][1][2] == '#'
                if (i, j) == (1, 2) and level + 1 in grids:
                    neigh += (grids[level+1][0][0] == '#') + \
                                (grids[level+1][0][1] == '#') + \
                                (grids[level+1][0][2] == '#') + \
                                (grids[level+1][0][3] == '#') + \
                                (grids[level+1][0][4] == '#')
                else:
                    neigh += grids[level][i+1][j] == '#' if i<4 else level - 1 in grids and grids[level-1][3][2] == '#'
                if (i, j) == (2, 3) and level + 1 in grids:
                    neigh += (grids[level+1][0][4] == '#') + \
                                (grids[level+1][1][4] == '#') + \
                                (grids[level+1][2][4] == '#') + \
                                (grids[level+1][3][4] == '#') + \
                                (grids[level+1][4][4] == '#')
                else:
                    neigh += grids[level][i][j-1] == '#' if j>0 else level - 1 in grids and grids[level-1][2][1] == '#'
                if (i, j) == (2, 1) and level + 1 in grids:
                    neigh += (grids[level+1][0][0] == '#') + \
                                (grids[level+1][1][0] == '#') + \
                                (grids[level+1][2][0] == '#') + \
                                (grids[level+1][3][0] == '#') + \
                                (grids[level+1][4][0] == '#')
                else:
                    neigh += grids[level][i][j+1] == '#' if j<4 else level - 1 in grids and grids[level-1][2][3] == '#'
                if grids[level][i][j] == '.' and neigh in [1, 2]:
                    row.append('#')
                elif grids[level][i][j] == '#' and neigh != 1:
                    row.append('.')
                else:
                    row.append(grids[level][i][j])
            new_grid.append(row)
        new_grids[level] = new_grid
    return new_grids

for i in range(200):
    grids = do_step(grids)

s = 0
for level in sorted(grids):
    for r in grids[level]:
        s += r.count('#')
print(s)
