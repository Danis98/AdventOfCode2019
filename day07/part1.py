import string

orig_tape = [int(x) for x in open("day07.input", "r").read().replace("\n", "").strip().split(",")]

instr_len = {
    1: 2,
    2: 2,
    3: 0,
    4: 1,
    5: 2,
    6: 2,
    7: 2,
    8: 2,
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

max_out = 0
for i in range(100000):
    dig = "%05d" % i
    if "".join(sorted(dig)) != "01234":
        continue
    in_list = [int(dig[int(i/2)]) if i%2==0 else -1 for i in range(10)]
    in_list[1] = 0
    in_ctr = 0
    for amp in range(5):
        pc = 0
        tape = list(orig_tape)

        while pc < len(tape):
            op = tape[pc] % 100
            p_modes = ("%d" % (tape[pc])).zfill(instr_len[op]+2)[:instr_len[op]][::-1]
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
                # tape[tape[pc+1]] = int(input())
                tape[tape[pc+1]] = in_list[in_ctr]
                in_ctr += 1
                pc += 2
            elif op == 4:
                if amp == 4:
                    max_out = max(max_out, p[0])
                else:
                    in_list[amp*2+3] = p[0]
                pc += 2
            elif op == 5:
                if p[0] != 0:
                    pc = p[1]
                else:
                    pc += 3
            elif op == 6:
                if p[0] == 0:
                    pc = p[1]
                else:
                    pc += 3
            elif op == 7:
                tape[tape[pc+3]] = 1 if p[0] < p[1] else 0
                pc += 4
            elif op == 8:
                tape[tape[pc+3]] = 1 if p[0] == p[1] else 0
                pc += 4
            else:
                print("AAAAAAA", pc, op)
                break
print(max_out)
