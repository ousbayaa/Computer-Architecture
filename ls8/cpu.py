"""CPU functionality."""

## LDI IS SAVE REGISTER
## PRN IS PRINT REGISTER


import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256 # bytes of mem
        self.reg = [0] * 8 # fixed size, max size of each reg
        self.pc = 0 # programme counter
        self.sp = 7
        self.FL = 0

        self.LDI = 0b10000010
        self.PRN = 0b01000111
        self.HLT = 0b00000001
        self.MUL = 0b10100010
        self.POP = 0b01000110
        self.PUSH = 0b01000101
        self.CALL = 0b01010000
        self.RET = 0b00010001
        self.ADD = 0b10100000
        self.CMP = 0b10100111
        self.JMP = 0b01010100
        self.JEQ = 0b01010101
        self.JNE = 0b01010110

    def ram_read(self, mar):
        return self.ram[mar] # memory address register

    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr # memory data register, 

    def load(self):
        """Load a program into memory."""

        address = 0

        if len(sys.argv) != 2:
            print("usage: ls8.py filename")
            sys.exit(1)

        try:
            with open(sys.argv[1]) as f:
                for line in f:
                    value = line.split("#")[0].strip()
                    if value == '':
                        continue
                    v = int(value, 2)
                    self.ram[address] = v
                    address += 1
        except FileNotFoundError:
            print(f"Error {sys.argv[1]}")
            sys.exit(1)

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]
        #
        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        IR = 0

        while True:
            # self.trace()
            IR = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if IR == self.HLT:
                exit()
            elif IR == self.LDI: #Load value into register
                self.reg[self.ram_read(self.pc + 1)] = self.ram_read(self.pc + 2)
                self.pc += 3
            elif IR == self.PRN: # Print
                print(self.reg[operand_a])
                self.pc += 2
            elif IR == self.MUL: # Multiple
                value = (self.reg[operand_a] * self.reg[operand_b]) & 0xFF
                self.reg[operand_a] = value
                self.pc += 3
            elif IR == self.POP: # Pop from stack
                value = self.ram_read(self.reg[self.sp])
                self.reg[self.sp] = self.reg[self.sp] + 1
                self.reg[operand_a] = value
                self.pc += 2
            elif IR == self.PUSH: # Push to stack
                self.reg[self.sp] -= 1
                self.ram[self.reg[self.sp]] = self.reg[operand_a]
                self.pc += 2
            elif IR == self.ADD: # Add 2 numbers
                value = (self.reg[operand_a] + self.reg[operand_b]) & 0xFF
                self.reg[operand_a] = value
                self.pc += 3
            elif IR == self.CALL: # Go to subroutine
                self.reg[self.sp] -= 1
                self.ram[self.reg[self.sp]] = self.pc + 2
                self.pc = self.reg[self.ram[self.pc + 1]]
            elif IR == self.RET: # return to original place in pc
                old_pc = self.ram[self.reg[self.sp]]
                self.reg[self.sp] = self.reg[self.sp] + 1
                self.pc = old_pc
            elif IR == self.CMP:
                if self.reg[operand_a] > self.reg[operand_b]:
                    self.FL = 0b00000010
                elif self.reg[operand_a] < self.reg[operand_b]:
                    self.FL = 0b00000100
                else:
                    self.FL = 0b00000001
                self.pc += 3
            elif IR == self.JMP:
                self.pc = self.reg[operand_a]
            elif IR == self.JEQ:
                if self.FL == 0b00000001:
                    self.pc = self.reg[operand_a]
                else:
                    self.pc += 2
            elif IR == self.JNE:
                if self.FL != 0b00000001:
                    self.pc = self.reg[operand_a]
                else:
                    self.pc += 2
            else:
                break
