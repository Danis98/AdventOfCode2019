import string

a, b = map(int, open("day04.input", "r").read().strip().split("-"))

print(sum(map(
    lambda s: "".join(sorted(s)) == s
                and 2 in map(lambda c: s.count(c), string.digits),
    map(lambda n: "%06d" % n, range(a, b+1))
)))
