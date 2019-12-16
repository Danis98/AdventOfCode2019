seq = list(map(int, open("day16.input", "r").read().strip())) * 10000
num_phases = 100

cum = [0]*len(seq)

def sum(a, b):
    global offset
    assert a >= offset
    if a > len(cum):
        s = 0
    elif a == 0:
        s = cum[b]
    else:
        s = cum[min(b, len(cum)-1)] - cum[a-1]
    return s

def dot_rep(lst, i):
    s = 0
    l = i
    while l < len(lst):
        s += sum(l,l+i)
        s -= sum(l+2*i+2, l+3*i+2)
        l += 4*(i+1)
    return abs(s) % 10

offset = int("".join(map(str, seq[:7])))

for i in range(len(seq)):
    if i == 0:
        cum[i] = seq[0]
    else:
        cum[i] = seq[i]+cum[i-1]
new_cum = [0] * len(seq)
new_seq = [0] * len(seq)
for n in range(1, num_phases+1):
    new_cum[offset-1] = 0
    for i in range(offset, len(seq)):
        new_seq[i] = dot_rep(seq, i)
        new_cum[i] = new_seq[i] + new_cum[i-1]
    seq, new_seq = new_seq, seq
    cum, new_cum = new_cum, cum
print("".join(map(str, seq[offset:offset+8])))
