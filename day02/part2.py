tape = [int(x) for x in open("day02.input", "r").read().strip().split(",")]
orig_tape = list(tape)

for x in range(100):
    for y in range(100):
        tape = list(orig_tape)
        pc = 0
        tape[1] = x
        tape[2] = y

        while True:
            op = tape[pc]
            if op == 99:
                break
            elif op == 1:
                tape[tape[pc+3]] = tape[tape[pc+1]] + tape[tape[pc+2]]
            elif op == 2:
                tape[tape[pc+3]] = tape[tape[pc+1]] * tape[tape[pc+2]]
            pc += 4

        if tape[0] == 19690720:
            print(100*x+y)
            break
