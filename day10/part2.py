import math

grid = open("day10.input", "r").read().strip().split()
asteroids = [(r, c) for (r, line) in enumerate(grid) for (c, e) in enumerate(line) if e == '#']

def angle_dist(a):
    return (math.atan2(a[1], -a[0]), a[0]**2+a[1]**2)

vlen = list(map(len, map(
    lambda cand: set(map(
        lambda a: math.atan2((a[1]-cand[1]), (a[0]-cand[0])),
        [a for a in asteroids if a != cand]
    )),
    asteroids
)))
cannon = asteroids[vlen.index(max(vlen))]

hook = (-0.5, 0)
targets = [(a[0]-cannon[0], a[1]-cannon[1]) for a in asteroids if a != cannon]
targets.append((-0.5, 0))
targets = sorted(targets, key=angle_dist)
idx = targets.index(hook)
targets = targets[idx+1:]+targets[:idx]

last = None
idx = 0
shots = []
while len(targets) > 0:
    shots.append(targets[idx])
    last = targets[idx]
    del targets[idx]
    if len(targets) == 0:
        break
    idx %= len(targets)
    next_idx = idx
    while angle_dist(last)[0] ==  angle_dist(targets[next_idx])[0]:
        next_idx = (next_idx+1)%len(targets)
        if next_idx == idx:
            break
    idx = next_idx
coord = list(map(lambda a: (a[0]+cannon[0], a[1]+cannon[1]), shots))[199]
print(coord[1]*100+coord[0])
