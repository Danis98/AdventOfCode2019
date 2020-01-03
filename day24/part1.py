grid = list(map(list, open("day24.input", "r").read().split()))

def do_step(grid):
    new_grid = []
    for i in range(5):
        row = []
        for j in range(5):
            neigh = 0
            neigh += grid[i-1][j] == '#' if i>0 else 0
            neigh += grid[i+1][j] == '#' if i<4 else 0
            neigh += grid[i][j-1] == '#' if j>0 else 0
            neigh += grid[i][j+1] == '#' if j<4 else 0
            if grid[i][j] == '.' and neigh in [1, 2]:
                row.append('#')
            elif grid[i][j] == '#' and neigh != 1:
                row.append('.')
            else:
                row.append(grid[i][j])
        new_grid.append(row)
    return new_grid

def stringify(grid):
    s = ""
    for r in range(5):
        s += "".join(grid[r])
    return s

vis = set()
while stringify(grid) not in vis:
    vis.add(stringify(grid))
    grid = do_step(grid)

diversity = 0
s = stringify(grid)
for i in range(25):
    if s[i] == '#':
        diversity += 2**i
print(diversity)
