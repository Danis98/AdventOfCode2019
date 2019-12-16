import time
tape = dict([(i, int(x)) for (i, x) in enumerate(open("day13.input", "r").read().replace("\n", "").strip().split(","))])

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

    def __init__(self, tape):
        self.tape = tape
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
            # print(self.pc, op, p_modes, p, self.rel_base)
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

tiles = {}
out_ctr = 0
x = None
y = None
score = 0
ball_pos = None
paddle_pos = None

def draw_screen():
    global score, paddle_pos, ball_pos
    bcount = 0
    for i in range(21):
        line = ""
        for j in range(37):
            if (j, i) not in tiles:
                line += " "
            else:
                line += " #X-O"[tiles[(j, i)]]
                if tiles[(j, i)] == 4:
                    ball_pos = (i, j)
                if tiles[(j, i)] == 3:
                    paddle_pos = (i, j)
                if tiles[(j, i)] == 2:
                    bcount += 1
        # print(line)
    # print("score: ", score)

def in_func():
    global ball_pos, paddle_pos
    draw_screen()
    # time.sleep(0.06)
    d = ball_pos[1] - paddle_pos[1]
    return 0 if d == 0 else (1 if d > 0 else -1)

def out_func(out):
    global tiles, x, y, out_ctr, score
    if out_ctr % 3 == 0:
        x = out
    elif out_ctr % 3 == 1:
        y = out
    else:
        if (x, y) == (-1, 0):
            score = out
        else:
            tiles[(x, y)] = out
    out_ctr += 1

tape[0] = 2
vm = IntcodeVM(tape)
vm.run(in_func, out_func)

print(score)
