raw = open("day08.input", "r").read().strip()
w = 25
h = 6
s = w * h

layers = [raw[s*i:s*(i+1)] for i in range(int(len(raw)/s))]

for i in range(h):
    line = ""
    for j in range(w):
        for l in range(len(layers)):
            pixel = int(layers[l][w*i+j])
            if pixel != 2:
                line += ' █'[pixel]
                break
    print(line)
