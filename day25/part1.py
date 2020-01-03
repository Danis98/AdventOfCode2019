tape = dict([(i, int(x)) for (i, x) in enumerate(open("day25.input", "r").read().replace("\n", "").strip().split(","))])

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
        self.exec = True

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
        while self.exec and not break_encountered:
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


def in_func():
    global in_s, in_ctr
    if in_ctr >= len(in_s):
        vm.exec = False
        return -1
    ret = ord(in_s[in_ctr])
    in_ctr += 1
    return ret

def out_func(out):
    global out_s, fail
    out_s += chr(out)
    if chr(out) == "\n":
        if "Alert!" in out_s:
            fail = True

take_obj = [
    "north\nnorth\nnorth\nwest\nsouth\nwest\ntake mutex\neast\nnorth\neast\nsouth\nsouth\nsouth\n",
    "south\nsouth\nsouth\nsouth\ntake festive hat\nnorth\nnorth\nnorth\nnorth\n",
    "south\ntake whirled peas\nnorth\n",
    "west\ntake pointer\neast\n",
    "north\ntake coin\nsouth\n",
    "north\nnorth\ntake astronaut ice cream\nsouth\nsouth\n",
    "north\nnorth\nnorth\nwest\ntake dark matter\neast\nsouth\nsouth\nsouth\n",
    "north\nnorth\nnorth\nwest\nsouth\ntake klein bottle\nnorth\neast\nsouth\nsouth\nsouth\n",
]

go_target = "north\nnorth\nnorth\nwest\nsouth\nwest\nwest\nsouth\neast\n"

for i in range(2**8):
    out_s = ""
    in_s = ""
    in_ctr = 0
    fail = False
    for j in range(8):
        if i>>j & 1:
            in_s += take_obj[j]
    in_s += go_target

    vm = IntcodeVM(tape)
    vm.run(in_func, out_func)

    if not fail:
        print(out_s.split()[-8])
        break
