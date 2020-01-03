moves = open("day22.input", "r").read().strip().split("\n")

slen = 10007

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

print(shuffle_pos(2019))
