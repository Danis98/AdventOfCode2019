import math

moves = open("day22.input", "r").read().strip().split("\n")

slen = 119315717514047
reps = 101741582076661

for i in range(len(moves)):
    move = moves[i]
    if move.startswith("deal into new stack"):
        moves[i] = (0,)
    elif move.startswith("deal with increment"):
        moves[i] = (1, int(move.split()[3]))
    elif move.startswith("cut"):
        moves[i] = (2, int(move.split()[1]))

def shuffle_pos(pos):
    global slen
    for move in moves:
        if move[0] == 0:
            pos *= -1
            pos -= 1
        elif move[0] == 1:
            pos *= move[1]
        elif move[0] == 2:
            pos -= move[1]
    pos %= slen
    return pos

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

def modpow(b, n, mod):
    p = 1
    while n > 0:
        if n % 2 == 1:
            p = (p*b)%mod
        n >>= 1
        b = (b*b)%mod
    return p

def sumpow(b, k, mod):
    res = 0
    e = 0
    k += 1
    digs = [(k>>i)&1 for i in range(math.floor(math.log2(k)), -1, -1)]
    if k == 0:
        return 0
    for d in digs:
        res = (res + res*modpow(b, e, mod)) % mod
        e <<= 1
        if d == 1:
            res = (1 + b * res) % mod
            e += 1
    return res - 1

s0 = shuffle_pos(0)
s1 = shuffle_pos(1)
diff = (s1 - s0) % slen
a = slen - s0
b = modinv(diff, slen)

orig = (sumpow(b, reps, slen)*a + modpow(b, reps, slen) * 2020) % slen
print(orig)
