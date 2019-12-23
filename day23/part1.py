import threading
tape = dict([(i, int(x)) for (i, x) in enumerate(open("day23.input", "r").read().replace("\n", "").strip().split(","))])

VM_NUM = 50

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
            if op not in self.instr_len:
                print("UNKNOWN OPCODE %r" % op)
                break
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

vms = [None for i in range(VM_NUM)]
initialized = [False for i in range(VM_NUM)]
packet_queue = [[] for i in range(VM_NUM)]
vm_buffer = [[] for i in range(VM_NUM)]
end = False

def nic_read(id):
    global packet_queue, initialized, end, vms
    if not initialized[id]:
        initialized[id] = True
        return id
    else:
        if len(packet_queue[id]) == 0:
            vms[id].exec = False
            return -1
        pack = packet_queue[id][0]
        if pack[0] is not None:
            ret = pack[0]
            packet_queue[id][0] = (None, pack[1])
            return ret
        packet_queue[id].pop(0)
        ret = pack[1]
        return ret

def nic_out(id, o):
    global vm_buffer, packet_queue, end
    vm_buffer[id].append(o)
    if len(vm_buffer[id]) == 3:
        if vm_buffer[id][0] == 255:
            print(vm_buffer[id][2])
            end = True
            return
        packet_queue[vm_buffer[id][0]].append((vm_buffer[id][1], vm_buffer[id][2]))
        vm_buffer[id] = []

for i in range(VM_NUM):
    vm = IntcodeVM(tape)
    vms[i] = vm

vm_ctr = 0
while not end:
    id = vm_ctr % VM_NUM
    vms[id].exec = True
    vms[id].run(lambda : nic_read(id), lambda o: nic_out(id, o))
    vm_ctr += 1
