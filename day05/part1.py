tape = [int(x) for x in open("day05.input", "r").read().replace("\n", "").strip().split(",")]

instr_len = {
    1: 2,
    2: 2,
    3: 0,
    4: 0,
    99: 0
}

def get_val(pc, i, p_mode):
    if p_mode == 0:
        return tape[tape[pc+i+1]]
    elif p_mode == 1:
        return tape[pc+i+1]
    else:
        print("AAAAAAA p_mode=", p_mode)
        return None

pc = 0

while True:
    op = tape[pc] % 100
    p_modes = ("%d" % (tape[pc]/100)).zfill(instr_len[op])[:instr_len[op]][::-1]
    p = [get_val(pc, i, int(p_modes[i])) for i in range(len(p_modes))]
    # print(op, p_modes, p)
    if op == 99:
        break
    elif op == 1:
        tape[tape[pc+3]] = p[0] + p[1]
        pc += 4
    elif op == 2:
        tape[tape[pc+3]] = p[0] * p[1]
        pc += 4
    elif op == 3:
        tape[tape[pc+1]] = int(input())
        pc += 2
    elif op == 4:
        print(tape[tape[pc+1]])
        pc += 2
    else:
        print("AAAAAAA", pc, op)
        break
