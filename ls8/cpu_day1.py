"""CPU functionality."""

import sys
import command

class CPU:
    """Main CPU class."""

    def __init__(self):
        """
        Construct a new CPU.
        Hint: Add list properties to the `CPU` class to hold 256 bytes of memory 
        and 8 general-purpose registers.
        """
        #DAY 1
        self.ram = [0] * 256 # 256 bytes of memory
        # Register is temporary storage area
        self.reg = [0] * 8   # 8 general-purpose registers
        self.pc  = 0         # set the program counter
        self.create_branchtable()

    def create_branchtable(self):
        self.branchtable = {}
        self.branchtable[command.LDI] = self.handle_LDI
        self.branchtable[command.PRN] = self.handle_PRN
        self.branchtable[command.HLT] = self.handle_HLT
        self.branchtable[command.MUL] = self.handle_MUL

    def ram_read(self, address):
            return self.ram[address]

    def ram_write(self, MAR, value):
        """
        MAR: memory address register
        """
        self.ram[MAR] = value


    def load(self):
        """Load a program into memory."""
        # writes pre-written commands in the program variable to RAM

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            0b10000010, # LDI R0,8
            0b00000000, # Register 0
            0b00001000, # 8 value
            0b01000111, # PRN R0
            0b00000000, # print(8 value)
            0b00000001, # HLT
        ]

        for instruction  in program:
            self.ram_write(address, instruction )
            # self.ram[address] = instruction 
            address += 1
 
    def load_file(self,filename):
        address = 0
        try:
            with open(filename) as f:
                for line in f:
                    # Ignore comments
                    comment_split = line.split("#")
                    # Strip out whitespace
                    num = comment_split[0].strip()
                    # Ignore blank lines
                    if num == '':
                        continue
                    instruction  = int(num,2)
                    self.ram[address] = instruction 
                    address += 1  
        except FileNotFoundError:
            print("File not found")
            sys.exit(2)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
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

    def handle_LDI(self,operand_a,operand_b):
        self.reg[operand_a] = operand_b
        self.pc += 3

    def handle_PRN(self,operand_a,operand_b):
        print(self.reg[operand_a])
        self.pc += 2

    def handle_MUL(self,operand_a,operand_b):
        self.alu('MUL',operand_a,operand_b)
        self.pc += 3

    def handle_HLT(self,operand_a,operand_b):
        self.running = False

    def run(self):
        """Run the CPU."""
        running = True
        while running:
            # after load 
            # the instructions loaded cycle through RAM
            instruction  = self.ram[self.pc]
            if instruction  == command.LDI:
                """Stop Program"""
                # Reg Location
                operand_a = self.ram_read(self.pc + 1)
                # Value
                operand_b = self.ram_read(self.pc + 2)
                self.reg[operand_a] = operand_b
                # counter is set 3 entries ahead 
                # one for the currently instruction , value and
                # other for the location
                self.pc += 3
            elif instruction  == command.PRN:
                # Reg Location
                operand_a = self.ram_read(self.pc + 1)
                print(self.reg[operand_a])
                # counter is set 2 entries ahead
                # 0ne for the currently instruction  and other
                # for the register location
                self.pc += 2
            elif instruction == command.MUL:
                # Reg0
                operand_a = self.ram_read(self.pc + 1)
                # Reg1
                operand_b = self.ram_read(self.pc + 2)
                self.alu('MUL',operand_a,operand_b)
                # counter is set 3 entries ahead 
                # one for the currently instruction , Register0 and
                # other for the Register1
                self.pc += 3
            elif instruction  == command.HLT:
                """Stop Program"""
                running = False
                self.pc += 1
            
            else:
                print(f"the program counter(PC): {self.pc} \n with the instruction: {self.ram_read(self.pc)}")
                sys.exit(1)
  


