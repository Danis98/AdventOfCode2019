pos = [[int(e.split("=")[1]) for e in line[1:-1].split(", ")] for line in open("day12.input", "r").read().strip().split("\n")]
vel = [[0, 0, 0] for i in range(4)]

energy = 0
for step in range(1000):
    # gravity
    for i in range(4):
        for j in range(i+1, 4):
            for axis in range(3):
                pi = pos[i][axis]
                pj = pos[j][axis]
                vel[i][axis] += 0 if pi == pj else (1 if pi < pj else -1)
                vel[j][axis] += 0 if pi == pj else (1 if pi > pj else -1)
    # velocity
    for i in range(4):
        for axis in range(3):
            pos[i][axis] += vel[i][axis]
    energy = 0
    for i in range(4):
        energy += sum(map(abs, pos[i])) * sum(map(abs, vel[i]))
print(energy)
