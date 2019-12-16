pos = [[int(e.split("=")[1]) for e in line[1:-1].split(", ")] for line in open("day12.input", "r").read().strip().split("\n")]
vel = [[0, 0, 0, 0] for i in range(3)]

pos = [[pos[i][axis] for i in range(4)] for axis in range(3)]
orig_pos = pos.copy()

def compute_gcd(x, y):
   while(y):
       x, y = y, x % y
   return x

def compute_lcm(x, y):
   lcm = (x*y)//compute_gcd(x,y)
   return lcm

vis_pos = [set() for i in range(3)]
for axis in range(3):
    vis_pos[axis].add(tuple(orig_pos[axis]))
step = 0
axis_done = [False, False, False]
cycles = []
while sum(axis_done) < 3:
    step += 1
    for axis in range(3):
        if axis_done[axis]:
            continue
        # gravity
        for i in range(4):
            for j in range(i+1, 4):
                pi = pos[axis][i]
                pj = pos[axis][j]
                vel[axis][i] += 0 if pi == pj else (1 if pi < pj else -1)
                vel[axis][j] += 0 if pi == pj else (1 if pi > pj else -1)
        # velocity
        for i in range(4):
            pos[axis][i] += vel[axis][i]
        if sum(map(abs, vel[axis])) == 0:
            if tuple(pos[axis]) in vis_pos[axis]:
                axis_done[axis] = True
                cycles.append(step)
            vis_pos[axis].add(tuple(pos[axis]))
    # print(pos)

print(compute_lcm(compute_lcm(cycles[0], cycles[1]), cycles[2]))
