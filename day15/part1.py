# -*- coding: utf-8 -*-
tape = dict([(i, int(x)) for (i, x) in enumerate(open("day15.input", "r").read().replace("\n", "").strip().split(","))])

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
    return int(input())

def stdout(out):
    print(out)

dir = {
    0: [-1, 0],
    1: [1, 0],
    2: [0, -1],
    3: [0, 1]
}

left_dir = [2, 3, 1, 0]
right_dir = [3, 2, 0, 1]

move_tree = {}
grid = {(0, 0): 0}
cur_pos = (0, 0)
last_move = None
next_move = 0
walld = 0
minX, maxX, minY, maxY = 0, 0, 0, 0

def clear(pos, d):
    nxt = (cur_pos[0]+dir[d][0], cur_pos[1]+dir[d][1])
    return nxt not in grid or grid[nxt] != -1

def make_move():
    global walld, last_move, cur_pos
    last_move = last_move if clear(cur_pos, walld) in grid else walld
    return last_move+1

def read_out(out):
    global last_move, next_move, walld, steps, cur_pos, minX, maxX, minY, maxY,\
    d, img, images, ctr
    next_pos = (cur_pos[0]+dir[last_move][0], cur_pos[1]+dir[last_move][1])
    minX = min(minX, next_pos[1])
    minY = min(minY, next_pos[0])
    maxX = max(maxX, next_pos[1])
    maxY = max(maxY, next_pos[0])
    if out == 0:
        # print("BONK :(")
        walld = left_dir[walld]
        grid[next_pos] = -1
    else:

        grid[next_pos] = min(grid[next_pos] if next_pos in grid else 10**12, grid[cur_pos]+1)
        walld = right_dir[last_move]
        if out == 2:
            print(grid[next_pos])
            grid[next_pos] = -2
            vm.halt = True
        cur_pos = next_pos
    # frame = ""
    # for r in range(minY, maxY+1):
    #     line = ""
    #     for c in range(minX, maxX+1):
    #         if (r, c) in grid and grid[(r, c)] == -2:
    #             line += "@"
    #         if (r, c) == cur_pos:
    #             line += "X"
    #         elif (r, c) not in grid:
    #             line += "?"
    #         else:
    #             if grid[(r, c)] == -1:
    #                 line += "█"
    #             else:
    #                 line += " "
    #     frame += line + "\n"
    # print(frame)


vm = IntcodeVM(tape)
vm.run(make_move, read_out)
