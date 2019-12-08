raw = open("day08.input", "r").read().strip()
w = 25
h = 6
s = w * h

layers = [raw[s*i:s*(i+1)] for i in range(int(len(raw)/s))]
zero_counts = list(map(lambda l: l.count('0'), layers))
min_idx = min([(v, i) for (i, v) in enumerate(zero_counts)])[1]

print(layers[min_idx].count('1')*layers[min_idx].count('2'))
