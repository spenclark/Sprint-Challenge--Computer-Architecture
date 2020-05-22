"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
POP = 0b01000110
PUSH = 0b01000101
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.register = [0] * 8
        self.ram = [0] * 256
        self.pc = 0
        self.sp = 7
        self.fl = 0b00000000
        self.instruction = {LDI: self.runLDI, PRN: self.runPRN, MUL: self.runMUL, HLT: self.runHLT}

    def load(self):
        """Load a program into memory."""

        address = 0

        with open(sys.argv[1]) as file:
            for i in file:
                i = i.split("#")[0].strip()
                if i == "":
                    continue
                instruction = int(i, 2)
                self.ram[address] = instruction
                address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.register[reg_a] += self.register[reg_b]
        # elif op == "SUB": etc
        elif op == "MUL":
            self.ram[reg_a] *= self.ram[reg_b]
        elif op == "CMP":
            #set e if a == b
            #lower e (set to 0000) if !=
            # set l reg a < b
            # set g if a > b
            if self.register[reg_a] == self.register[reg_b]:
                self.fl = 0b00000001
            if self.register[reg_a] != self.register[reg_b]:
                self.fl = 0b00000000
            if self.register[reg_a] < self.register[reg_b]:
                self.fl = 0b00000100
            if self.register[reg_a] > self.register[reg_b]:
                self.fl = 0b00000010
            return None
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        # print(f"TRACE: %02X | %02X %02X %02X |" % (
        #     self.pc,
        #     # self.fl,
        #     # self.ie,
        #     self.ram_read(self.pc),
        #     self.ram_read(self.pc + 1),
        #     self.ram_read(self.pc + 2)
        # ), end='')

        # for i in range(8):
        #     print(" %02X" % self.register[i], end='')

    def runLDI(self):
        operand_a = self.ram[self.pc + 1]
        operand_b = self.ram[self.pc + 2]
        self.ram_write(operand_a, operand_b)
        self.pc += 3
    
    def runHLT(self):
        self.run.on = False

    def runPRN(self): 
        location = self.ram[self.pc + 1]
        print(self.ram_read(location))
        self.pc += 1

    def runMUL(self):
        operand_a = self.ram[self.pc + 1]
        operand_b = self.ram[self.pc + 2]
        self.alu("MUL", operand_a, operand_b)
        self.pc += 1

    def ram_read(self, loc):
        return self.ram[loc]

    def ram_write(self, loc, value):
        self.ram[loc] = value


    def run(self):
        """Run the CPU."""
        on = True
        while on:
            inst = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            if inst == LDI:
                self.register[operand_a] = operand_b
                self.pc += 3
            elif inst == PRN:
                print(self.register[operand_a])
                self.pc += 2
            elif inst == MUL:
                self.alu("MUL", operand_a, operand_b)
                self.pc += 3
            elif inst == HLT:
                on = False
            elif inst == PUSH:
                self.register[self.sp] -= 1
                self.ram_write(self.register[self.sp], self.register[operand_a])
                self.pc += 2

            elif inst == POP:
                last_val = self.ram_read(self.register[self.sp])
                self.register[operand_a] = last_val
                self.register[self.sp] += 1
                self.pc += 2
            else:
                print(f"We have failed {inst}, maybe try another input. Turning off...")
                on = False
