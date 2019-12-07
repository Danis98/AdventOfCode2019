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

def get_val(tape, pc, i, p_mode):
    if p_mode == 0:
        return tape[tape[pc+i+1]]
    elif p_mode == 1:
        return tape[pc+i+1]
    else:
        print("AAAAAAA p_mode=", p_mode)
        return None

def run_until_wait(th_id, tape, pc, in_queue, out_queue):
    while pc < len(tape):
        op = tape[pc] % 100
        p_modes = ("%d" % (tape[pc])).zfill(instr_len[op]+2)[:instr_len[op]][::-1]
        p = [get_val(tape, pc, i, int(p_modes[i])) for i in range(len(p_modes))]
        # print(op, p_modes, p)
        if op == 99:
            return -1
        elif op == 1:
            tape[tape[pc+3]] = p[0] + p[1]
            pc += 4
        elif op == 2:
            tape[tape[pc+3]] = p[0] * p[1]
            pc += 4
        elif op == 3:
            # tape[tape[pc+1]] = int(input())
            if len(in_queue) == 0:
                return pc
            tape[tape[pc+1]] = in_queue.pop(0)
            pc += 2
        elif op == 4:
            # print(pc, p[0])
            out_queue.append(p[0])
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
    return -1

max_out = 0
for i in range(100000):
    dig = "%05d" % i
    if "".join(sorted(dig)) != "56789":
        continue
    in_list = [[int(dig[i])] for i in range(5)]
    in_list[0].append(0)
    threads = {
        0: [0, list(orig_tape), 0, in_list[0]],
        1: [1, list(orig_tape), 0, in_list[1]],
        2: [2, list(orig_tape), 0, in_list[2]],
        3: [3, list(orig_tape), 0, in_list[3]],
        4: [4, list(orig_tape), 0, in_list[4]]
    }
    while True:
        halt = False
        for th in threads:
            # print("stepping thread %d from %d" % (th, threads[th][2]))
            if threads[th][2] == -1:
                halt = True
                continue
            out = []
            threads[th][2] = run_until_wait(*threads[th], out)
            threads[(th+1)%len(threads)][3] += out
        if halt:
            break
        max_out = max(threads[0][3][0], max_out)
print(max_out)
