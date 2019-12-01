modules = map(lambda x: int(x), open("day01.input", "r").read().strip().split())

def get_fuel(m):
    fuel = 0
    cur = m
    while cur > 6:
        f = int(cur / 3) - 2
        fuel += f
        cur = f
    return fuel

print(sum(map(get_fuel, modules)))
