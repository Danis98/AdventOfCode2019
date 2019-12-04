a, b = map(int, open("day04.input", "r").read().strip().split("-"))

print(sum(map(
    lambda s: "".join(sorted(s)) == s
                and len(set(s)) != len(s),
    map(lambda n: "%06d" % n, range(a, b+1))
)))
