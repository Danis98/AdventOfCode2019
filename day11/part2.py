tape = dict([(i, int(x)) for (i, x) in enumerate(open("day11.input", "r").read().replace("\n", "").strip().split(","))])

dir = {
    0: [1, 0],
    1: [0, 1],
    2: [-1, 0],
    3: [0, -1]
}

grid = {}
vis = set((0, 0, 0, 0))

pos = (0, 0)
cur_dir = 0
out_ctr = 0
grid[pos] = 1

def read_panel():
    if pos not in grid:
        return 0
    return grid[pos]

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

def get_addr(pc, i, p_mode):
    global rel_base
    if pc+i+1 not in tape:
        tape[pc+i+1] = 0
    if p_mode == 0:
        if tape[pc+i+1] not in tape:
            tape[tape[pc+i+1]] = 0
        return tape[pc+i+1]
    elif p_mode == 1:
        return pc+i+1
    elif p_mode == 2:
        if tape[pc+i+1] + rel_base not in tape:
            tape[tape[pc+i+1] + rel_base] = 0
        return tape[pc+i+1] + rel_base
    else:
        print("AAAAAAA p_mode=", p_mode)
        return None

pc = 0
rel_base = 0

while True:
    op = tape[pc] % 100
    p_modes = ("%d" % (tape[pc])).zfill(instr_len[op]+2)[:instr_len[op]][::-1]
    p = [get_addr(pc, i, int(p_modes[i])) for i in range(len(p_modes))]
    # print(pc, op, p_modes, p, rel_base)
    if op == 99:
        break
    elif op == 1:
        tape[p[2]] = tape[p[0]] + tape[p[1]]
        pc += 4
    elif op == 2:
        tape[p[2]] = tape[p[0]] * tape[p[1]]
        pc += 4
    elif op == 3:
        tape[p[0]] = read_panel()
        pc += 2
    elif op == 4:
        if out_ctr % 2 == 0:
            grid[pos] = tape[p[0]]
        else:
            cur_dir = (cur_dir + (3 if tape[p[0]] == 0 else 1)) % 4
            pos = (pos[0] + dir[cur_dir][0], pos[1] + dir[cur_dir][1])
            # print(pos[0], pos[1], cur_dir, read_panel())
            # print(grid)
            # if (pos[0], pos[1], cur_dir, read_panel()) in vis:
                # break
            vis.add((pos[0], pos[1], cur_dir, read_panel()))
        out_ctr += 1
        pc += 2
    elif op == 5:
        if tape[p[0]] != 0:
            pc = tape[p[1]]
        else:
            pc += 3
    elif op == 6:
        if tape[p[0]] == 0:
            pc = tape[p[1]]
        else:
            pc += 3
    elif op == 7:
        tape[p[2]] = 1 if tape[p[0]] < tape[p[1]] else 0
        pc += 4
    elif op == 8:
        tape[p[2]] = 1 if tape[p[0]] == tape[p[1]] else 0
        pc += 4
    elif op == 9:
        rel_base += tape[p[0]]
        pc += 2
    else:
        print("AAAAAAA", pc, op)
        break

for r in range(6):
    line = ""
    for c in range(42):
        line += ' █'[grid[(-r, c)] if (-r, c) in grid else 0]
    print(line)
