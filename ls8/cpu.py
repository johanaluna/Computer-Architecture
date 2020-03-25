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
        self.ram = [0] * 256            # 256 bytes of memory
        # Register is temporary storage
        self.reg = [0] * 8              # 8 general-purpose registers
        self.reg[7] = 0xF4
        self.pc  = 0                    # set the program counter
        self.create_branchtable()
        # R5 is reserved as the interrupt mask (IM)
        
        # R6 is reserved as the interrupt status (IS)
        
        # R7 is reserved as the stack pointer (SP)
        self.sp = 7
        self.fl = 0

    def create_branchtable(self):
        self.branchtable = {}
        filename = 'command.py'
        with open(filename) as f:
            for line in f:
                # Ignore comments
                comment_split = line.split("=")
                # Strip out whitespace
                command_name = comment_split[0].strip()
                command_value= comment_split[1].replace("\n","")
                # Ignore blank lines
                name_function = 'handle_'+ command_name
                function = getattr(self, name_function)  
                self.branchtable[int(command_value,2)] = function


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
        """
        ALU operations.
        link: https://python-reference.readthedocs.io/en/latest/docs/operators/#assignment-operators
        """

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "DIV":
            self.reg[reg_a] /= self.reg[reg_b]
        elif op == "MOD":
            self.reg[reg_a] %= self.reg[reg_b]

        elif op == "INC":
            self.reg[reg_a] += 1
        elif op == "DEC":
            self.reg[reg_a] -= 1

        elif op == "CMP":
            if self.reg[reg_a] == self.reg[reg_b]:
                # set the E flag to 1
                self.fl = 0b00000001
            elif self.reg[reg_a] < self.reg[reg_b]:
                # set the L flag to 1
                self.fl = 0b00000100
            else:
                # set the G flag to 1
                self.fl = 0b00000010

        elif op == "AND":
            self.reg[reg_a] &= self.reg[reg_b]
        elif op == "NOT":
            self.reg[reg_a] =  ~self.reg[reg_b]
        elif op == "OR":
            self.reg[reg_a] |= self.reg[reg_b]
        elif op == "XOR":
            self.reg[reg_a] ^= self.reg[reg_b]
        elif op == "SHL":
            self.reg[reg_a] <<= self.reg[reg_b]
        elif op == "SHR":
            self.reg[reg_a] >>= self.reg[reg_b]
        
        
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

    """
    The SP points at the value at the top of
    the stack (most recently pushed),
    or at address F4 if the stack is empty.
    """
    def handle_PUSH(self,operand_a,operand_b):
        """
        Link:
        https://www.youtube.com/watch?v=d-2Peb3pCBg
        Push Data:
        - write data above the top
        - update top
        """
        # decrement the SP
        self.reg[self.sp] -= 1
        self.ram_write(self.reg[self.sp], self.reg[operand_a])
        self.pc += 2

    def handle_POP(self,operand_a,operand_b):
        """
        POP Data
        - Read data on top stack
        - Update top
        """
        # get last value: self.ram_read(self.reg[self.sp])
        self.reg[operand_a] = self.ram_read(self.reg[self.sp])
        # increment the SP
        self.reg[self.sp] += 1
        self.pc += 2


    def handle_LD(self,operand_a,operand_b):
        #Loads registerA with the value at the memory address stored in registerB
        self.reg[operand_a] = self.ram_read(self.reg[operand_b])

    def handle_PRA(self,operand_a,operand_b):
        print(chr(self.reg[operand_a]), end="")

        
    def run(self):
        self.running = True
        while self.running:
            ir = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            self.branchtable[ir](operand_a,operand_b)
            



