import math

grid = open("day10.input", "r").read().strip().split()
asteroids = [(r, c) for (r, line) in enumerate(grid) for (c, e) in enumerate(line) if e == '#']

print(max(map(len, map(
    lambda cand: set(map(
        lambda a: math.atan2((a[1]-cand[1]), (a[0]-cand[0])),
        [a for a in asteroids if a != cand]
    )),
    asteroids
))))
