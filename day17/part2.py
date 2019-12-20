tape = dict([(i, int(x)) for (i, x) in enumerate(open("day17.input", "r").read().replace("\n", "").strip().split(","))])

class IntcodeVM:
    instr_len = {
        1: 3,
        2: 3,
        3: 1,
        4: 1,
        5: 2,
        6: 2,
        7: 3,
        8: 3,
        9: 1,
        99: 0
    }

    memo = {
        1: "add",
        2: "mul",
        3: "in",
        4: "out",
        5: "jnz",
        6: "jz",
        7: "lt",
        8: "eq",
        9: "base",
        99: "halt"
    }

    def __init__(self, tape):
        self.tape = tape.copy()
        self.pc = 0
        self.rel_base = 0
        self.breakpoints = set()

    def get_addr(self, addr, p_mode):
        if addr not in self.tape:
            self.tape[addr] = 0
        if p_mode == 0:
            if self.tape[addr] not in self.tape:
                self.tape[self.tape[addr]] = 0
            return self.tape[addr]
        elif p_mode == 1:
            return addr
        elif p_mode == 2:
            if self.tape[addr] + self.rel_base not in self.tape:
                self.tape[self.tape[addr] + self.rel_base] = 0
            return self.tape[addr] + self.rel_base
        else:
            print("AAAAAAA p_mode=", p_mode)
            return None

    def run(self, in_func, out_func):
        break_encountered = False
        while not break_encountered:
            op = self.tape[self.pc] % 100
            p_modes = ("%d" % (self.tape[self.pc])).zfill(self.instr_len[op]+2)[:self.instr_len[op]][::-1]
            p = [self.get_addr(self.pc+i+1, int(p_modes[i])) for i in range(len(p_modes))]
            # print(self.pc, op, self.memo[op], p_modes, [(pe, self.tape[pe]) for pe in p], self.rel_base)
            if self.pc in self.breakpoints:
                break_encountered = True
            if op == 99:
                break
            elif op == 1:
                self.tape[p[2]] = self.tape[p[0]] + self.tape[p[1]]
                self.pc += 4
            elif op == 2:
                self.tape[p[2]] = self.tape[p[0]] * self.tape[p[1]]
                self.pc += 4
            elif op == 3:
                self.tape[p[0]] = in_func()
                self.pc += 2
            elif op == 4:
                out_func(self.tape[p[0]])
                self.pc += 2
            elif op == 5:
                if self.tape[p[0]] != 0:
                    self.pc = self.tape[p[1]]
                else:
                    self.pc += 3
            elif op == 6:
                if self.tape[p[0]] == 0:
                    self.pc = self.tape[p[1]]
                else:
                    self.pc += 3
            elif op == 7:
                self.tape[p[2]] = 1 if self.tape[p[0]] < self.tape[p[1]] else 0
                self.pc += 4
            elif op == 8:
                self.tape[p[2]] = 1 if self.tape[p[0]] == self.tape[p[1]] else 0
                self.pc += 4
            elif op == 9:
                self.rel_base += self.tape[p[0]]
                self.pc += 2
            else:
                print("AAAAAAA", self.pc, op)
                break
def stdin():
    global str, ctr
    ch = ord(str[ctr])
    ctr += 1
    return ch

grid = {}
line = []
pos = None
d = None
dir = {
    0: [-1, 0],
    1: [0, 1],
    2: [1, 0],
    3: [0, -1]
}
r, c = 0, 0
def stdout(out):
    global grid, line, pos, d, r, c
    if out > 255:
        print(out)
        return
    ch = chr(out)
    if ch == '\n':
        r += 1
        c = 0
    else:
        if ch in 'Xv^<>':
            pos = (r, c)
            if ch == 'X':
                grid[(r, c)] = '.'
            else:
                grid[(r, c)] = '#'
                d = '^>v<'.index(ch)
        else:
            grid[(r, c)] = ch
        c += 1

vm = IntcodeVM(tape)
vm.run(stdin, stdout)

def check_rot(p, d):
    s = (p[0]+dir[d][0], p[1]+dir[d][1])
    l = (p[0]+dir[(d+3)%4][0], p[1]+dir[(d+3)%4][1])
    r = (p[0]+dir[(d+1)%4][0], p[1]+dir[(d+1)%4][1])
    if s in grid and grid[s] == '#':
        return 'S'
    if l in grid and grid[l] == '#':
        return 'L'
    if r in grid and grid[r] == '#':
        return 'R'
    return 'E'

moves = []
while True:
    rot = check_rot(pos, d)
    if rot == 'E':
        break
    if rot in 'RL':
        moves.append(rot)
        d = (d + 2*'RL'.index(rot) + 1) % 4
    dst = 0
    nxt = (pos[0]+dir[d][0], pos[1]+dir[d][1])
    while nxt in grid and grid[nxt] == '#':
        dst += 1
        nxt = (nxt[0]+dir[d][0], nxt[1]+dir[d][1])
    moves.append(dst)
    pos = (pos[0]+dir[d][0]*dst, pos[1]+dir[d][1]*dst)

print(moves)

A = 'R,12,L,10,L,10'
B = 'L,6,L,12,R,12,L,4'
C = 'L,12,R,12,L,6'
main = "A,B,A,B,C,B,C,A,C,C"

str = main + "\n" + A + "\n" + B + "\n" + C + "\nn\n"
ctr = 0

tape[0] = 2
vm = IntcodeVM(tape)
vm.run(stdin, stdout)
