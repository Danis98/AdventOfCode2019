# -*- coding: utf-8 -*-
tape = dict([(i, int(x)) for (i, x) in enumerate(open("day19.input", "r").read().replace("\n", "").strip().split(","))])

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
        self.halt = False

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
        while not break_encountered and not self.halt:
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
    global ctr
    coord = int(in_q[ctr])
    ctr += 1
    return coord

def stdout(out):
    global beam
    beam = out

in_q = []
ctr = 0
beam = 0
a, b = 0, 10000
sq_len = 100
while a < b:
    mid = (a+b)//2
    fit = False
    y = mid
    for x in range(y, 2*y):
        in_q = [x, y]
        ctr = 0
        vm = IntcodeVM(tape)
        vm.run(stdin, stdout)
        if beam == 0:
            continue
        in_q = [x, y+sq_len-1]
        ctr = 0
        vm = IntcodeVM(tape)
        vm.run(stdin, stdout)
        if beam == 0:
            continue
        in_q = [x+sq_len-1, y]
        ctr = 0
        vm = IntcodeVM(tape)
        vm.run(stdin, stdout)
        if beam == 0:
            continue
        fit = True
        code = x * 10000 + y
        break
    if fit:
        b = mid
    else:
        a = mid + 1
print(code)
