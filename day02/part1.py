tape = [int(x) for x in open("day02.input", "r").read().strip().split(",")]

pc = 0

tape[1] = 12
tape[2] = 2

while True:
    op = tape[pc]
    if op == 99:
        break
    elif op == 1:
        tape[tape[pc+3]] = tape[tape[pc+1]] + tape[tape[pc+2]]
    elif op == 2:
        tape[tape[pc+3]] = tape[tape[pc+1]] * tape[tape[pc+2]]
    pc += 4

print(tape[0])
